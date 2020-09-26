from dataclasses import dataclass, is_dataclass, fields
from inspect import signature
from typing import Union, Callable, TypeVar, Dict

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


def is_init(fi: FieldInfo):
    """ If this is a dataclass field with init=True, skip """

    if fi.init is False:
        raise SkipField()


def is_in_props(fi: FieldInfo, p: Dict):
    if p and fi.field_name in p:
        prop_value = p[fi.field_name]
        raise FoundValueField(prop_value)


def is_container(fi: FieldInfo, c: ServiceContainer):
    """ Is the asked-for field type the container? """

    if fi.field_type is ServiceContainer:
        raise FoundValueField(c)


def make_pipeline(fi: FieldInfo, c: ServiceContainer):
    """ If pipeline, process it, else, bail out """

    if not fi.pipeline:
        fv = c.get(fi.field_type)
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

    def __call__(self, target: Union[T, Callable], **kwargs) -> T:
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
                function_field_info_factory(param)
                for param in parameters
            ]

        # Go through each field and apply policies
        for field_info in field_infos:
            field_name = field_info.field_name
            field_type = field_info.field_type
            pipeline = field_info.pipeline

            try:
                is_init(field_info)
                is_in_props(field_info, props)
                is_container(field_info, self.container)
                make_pipeline(field_info, self.container)
            except SkipField:
                continue
            except FoundValueField as exc:
                args[field_name] = exc.value
                continue

        return target(**args)
