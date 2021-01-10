import sys
import typing
from dataclasses import dataclass, is_dataclass, fields
from inspect import signature, getmodule, isclass
from typing import Dict, NamedTuple, Tuple, Type, Any, Optional, Callable

from wired import ServiceContainer
from wired_injector.field_info import (
    function_field_info_factory,
    dataclass_field_info_factory,
    FieldInfo,
)
from wired_injector.pipeline import Pipeline

# get_type_hints is augmented in Python 3.9. We need to use
# typing_extensions if not running on an older version
if sys.version_info[:3] >= (3, 9):
    from typing import get_type_hints
else:  # pragma: no cover
    from typing_extensions import get_type_hints


class SkipField(BaseException):
    """Not part of construction.

    Tell the injector that this field should not be part of
    construction. Used for example on a dataclass field with
    field(init=False).
    """

    pass


class FoundValueField(BaseException):
    """Found a value for the field.

    If a rule matches a condition and finds a value, return
    the value as the exception value, then put it in the
    args for that field.
    """

    def __init__(self, *args):
        self.value = args[0] if args else None


class FieldIsInit(NamedTuple):
    """ If this is a dataclass field with init=False, skip """

    field_info: FieldInfo
    props: Dict
    container: ServiceContainer
    system_props: Optional[Dict] = None
    target: Optional[Callable] = None

    def __call__(self):
        if self.field_info.init is False:
            raise SkipField()


class FieldIsInProps(NamedTuple):
    """ If field in passed-in props or system props, return value """

    field_info: FieldInfo
    props: Dict
    container: ServiceContainer
    system_props: Optional[Dict] = None
    target: Optional[Callable] = None

    def __call__(self):
        if self.props and self.field_info.field_name in self.props:
            # Props have precedence
            prop_value = self.props[self.field_info.field_name]
            raise FoundValueField(prop_value)
        elif (
            self.system_props
            and self.field_info.field_name in self.system_props
        ):
            # If the "system" passes in props behind the scenes, use it
            prop_value = self.system_props[self.field_info.field_name]
            raise FoundValueField(prop_value)


class FieldIsContainer(NamedTuple):
    """ If the field is asking for a ServiceContainer, return it """

    field_info: FieldInfo
    props: Dict
    container: ServiceContainer
    system_props: Optional[Dict] = None
    target: Optional[Callable] = None

    def __call__(self):
        if self.field_info.field_type is ServiceContainer:
            raise FoundValueField(self.container)


class FieldMakePipeline(NamedTuple):
    """ If pipeline, process it, else, bail out """

    field_info: FieldInfo
    props: Dict
    container: ServiceContainer
    system_props: Optional[Dict] = None
    target: Optional[Callable] = None

    def __call__(self):
        fi = self.field_info
        c = self.container
        if not fi.operators:
            if getmodule(fi.field_type) is typing:
                # Test this because, when you have a field like:
                #   names: Tuple[str, ...] = ('Name 1',)  # noqa: E800
                # ...then wired tries to do obj.__qualname__ and fails
                raise SkipField()
            try:
                fv = c.get(fi.field_type)
            except (TypeError, LookupError):
                # We're probably looking up something like str. Since
                # we might have a default value, let's skip this.
                raise SkipField()
        else:
            pipeline = Pipeline(
                # field_info=self.field_info,
                container=c,
                start=fi.field_type,
                target=self.target,
            )
            fv = pipeline(*fi.operators)
        raise FoundValueField(fv)


@dataclass
class Injector:
    """Introspect targets and call/construct with container data.

    The injector is a factory in a container which fetch the data
    needed for a factory, then call it. The injector is a per-container
    service.


    """

    container: ServiceContainer
    rules: Tuple[Type[Any], ...] = (
        FieldIsInit,
        FieldIsInProps,
        FieldIsContainer,
        FieldMakePipeline,
    )

    def __call__(
        self,
        target: Any,
        system_props: Optional[typing.Mapping[str, Any]] = None,
        **kwargs,
    ) -> Any:

        args = {}
        props = kwargs
        if is_dataclass(target):
            type_hints = get_type_hints(target, include_extras=True)
            # noinspection PyDataclass
            fields_mapping = {f.name: f for f in fields(target)}
            field_infos = [
                dataclass_field_info_factory(fields_mapping[field_name])
                for field_name in type_hints
            ]
        else:
            sig = signature(target)
            parameters = sig.parameters.values()
            field_infos = [
                function_field_info_factory(param) for param in parameters
            ]

        # Go through each field and apply policies
        for field_info in field_infos:
            field_name = field_info.field_name

            try:
                for rule in self.rules:
                    # noinspection PyArgumentList
                    r = rule(
                        field_info, props, self.container, system_props, target
                    )
                    # noinspection PyCallingNonCallable
                    r()
            except SkipField:
                continue
            except FoundValueField as exc:
                this_value = exc.value
                if isclass(this_value):
                    # This "service" is actually injectable, instead of
                    # a plain factory. At the moment, we just have a class.
                    # Use this injector instance to turn it into an instance.
                    this_value = self(this_value)
                args[field_name] = this_value
                continue

        return target(**args)
