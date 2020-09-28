from dataclasses import dataclass, is_dataclass, fields
from inspect import signature, getmodule
import typing
from typing import Union, Callable, TypeVar, Dict, NamedTuple, Tuple, Type, Any, Optional

from wired import ServiceContainer
from wired_injector.field_info import function_field_info_factory, dataclass_field_info_factory, FieldInfo
from wired_injector.operators import process_pipeline

try:
    from typing import Annotated
    from typing import get_type_hints
except ImportError:
    # Need the updated get_type_hints which allows include_extras=True
    from typing_extensions import Annotated, get_type_hints

T = TypeVar('T')


class SkipField(BaseException):
    """ Not part of construction.

    Tell the injector that this field should not be part of
    construction. Used for example on a dataclass field with
    field(init=False).
    """
    pass


class FoundValueField(BaseException):
    """ Found a value for the field.

    If a rule matches a condition and finds a value, return
    the value as the exception value, then put it in the
    args for that field.
    """

    def __init__(self, *args):
        self.value = args[0] if args else None


class FieldIsInit(NamedTuple):
    """ If this is a dataclass field with init=True, skip """

    field_info: FieldInfo
    props: Dict
    container: ServiceContainer
    system_props: Optional[Dict] = None

    def __call__(self):
        if self.field_info.init is False:
            raise SkipField()


class FieldIsInProps(NamedTuple):
    """ If field in passed-in props or system props, return value """

    field_info: FieldInfo
    props: Dict
    container: ServiceContainer
    system_props: Optional[Dict] = None

    def __call__(self):
        if self.props and self.field_info.field_name in self.props:
            # Props have precedence
            prop_value = self.props[self.field_info.field_name]
            raise FoundValueField(prop_value)
        elif self.system_props and self.field_info.field_name in self.system_props:
            # If the "system" passes in props behind the scenes, use it
            prop_value = self.system_props[self.field_info.field_name]
            raise FoundValueField(prop_value)


class FieldIsContainer(NamedTuple):
    """ If the field is asking for a ServiceContainer, return it """

    field_info: FieldInfo
    props: Dict
    container: ServiceContainer
    system_props: Optional[Dict] = None

    def __call__(self):
        if self.field_info.field_type is ServiceContainer:
            raise FoundValueField(self.container)


class FieldMakePipeline(NamedTuple):
    """ If pipeline, process it, else, bail out """

    field_info: FieldInfo
    props: Dict
    container: ServiceContainer
    system_props: Optional[Dict] = None

    def __call__(self):
        fi = self.field_info
        c = self.container
        if not fi.pipeline:
            if getmodule(fi.field_type) is typing:
                # Test this because, when you have a field like:
                #   names: Tuple[str, ...] = ('Name 1',)
                # ...then wired tries to do obj.__qualname__ and fails
                raise SkipField()
            try:
                fv = c.get(fi.field_type)
            except (TypeError, LookupError):
                # We're probably looking up something like str. Since
                # we might have a default value, let's skip this.
                raise SkipField()
        else:
            fv = process_pipeline(
                c,
                fi.pipeline,
                fi.field_type
            )
        raise FoundValueField(fv)


@dataclass
class Injector:
    container: ServiceContainer
    rules: Tuple[Type[NamedTuple], ...] = (
        FieldIsInit,
        FieldIsInProps,
        FieldIsContainer,
        FieldMakePipeline,
    )

    def __call__(
            self,
            target: Union[T, Callable],
            system_props: Dict[str, Any] = None,
            **kwargs,
    ) -> T:
        args = {}
        props = kwargs
        if is_dataclass(target):
            type_hints = get_type_hints(target, include_extras=True)
            fields_mapping = {f.name: f for f in fields(target)}
            field_infos = [
                dataclass_field_info_factory(fields_mapping[field_name])
                for field_name in type_hints
            ]
        else:
            sig = signature(target)
            parameters = sig.parameters.values()
            field_infos = [
                function_field_info_factory(param)
                for param in parameters
            ]

        # Go through each field and apply policies
        for field_info in field_infos:
            field_name = field_info.field_name
            field_type = field_info.field_type
            pipeline = field_info.pipeline

            try:
                for rule in self.rules:
                    # noinspection PyArgumentList
                    r = rule(field_info, props, self.container, system_props)
                    # noinspection PyCallingNonCallable
                    r()
            except SkipField:
                continue
            except FoundValueField as exc:
                args[field_name] = exc.value
                continue

        return target(**args)
