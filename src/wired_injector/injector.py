from dataclasses import dataclass, is_dataclass, fields
from inspect import signature
from typing import Union, Type, Callable

from wired import ServiceContainer
from wired_injector.field_info import function_field_info_factory, dataclass_field_info_factory

try:
    from typing import Annotated
    from typing import get_type_hints
except ImportError:
    # Need the updated get_type_hints which allows include_extras=True
    from typing_extensions import Annotated, get_type_hints


@dataclass
class Injector:
    container: ServiceContainer

    def __call__(self, target: Union[Type, Callable], **kwargs):
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

            # ----  Special cases to bail out early on
            # Field has init=False which means, don't initialize
            if field_info.init is False:
                continue

            # Next-highest precedence: this field occurs in the passed-in
            # props. Check there first.
            if props and field_name in props:
                prop_value = props[field_name]
                args[field_name] = props[field_name]
                continue

            args[field_name] = self.container

        return target(**args)
