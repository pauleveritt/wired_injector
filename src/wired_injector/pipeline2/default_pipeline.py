import sys
from dataclasses import dataclass, is_dataclass, fields, field
from inspect import signature
from typing import Any, Optional, Dict, Callable, Sequence, Tuple, Type

from wired_injector.field_info import dataclass_field_info_factory, function_field_info_factory
from . import Result
from .results import (
    Error,
    Found,
    Init,
    NotFound,
    Skip,
)
from .rules import IsInit, IsInProps, IsContainer, AnnotationPipeline

from . import Container, FieldInfo

# get_type_hints is augmented in Python 3.9. We need to use
# typing_extensions if not running on an older version
if sys.version_info[:3] >= (3, 9):
    from typing import get_type_hints
else:  # pragma: no cover
    from typing_extensions import get_type_hints

Target = Callable[..., Any]

RULES: Tuple[Type[Any], ...] = (
    IsInit,
    IsInProps,
    IsContainer,
    AnnotationPipeline,
)


@dataclass
class DefaultPipeline:
    """
    Bundled implementation of the Pipeline protocol.
    """

    container: Container
    field_infos: Sequence[FieldInfo] = field(init=False)
    props: Dict[str, Any]
    target: Target
    system_props: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """ For the target, extract each field into sequence of field info """

        target = self.target
        if is_dataclass(target):
            type_hints = get_type_hints(target, include_extras=True)
            # noinspection PyDataclass
            fields_mapping = {f.name: f for f in fields(target)}
            self.field_infos = [
                dataclass_field_info_factory(fields_mapping[field_name])
                for field_name in type_hints
            ]
        else:
            sig = signature(target)
            parameters = sig.parameters.values()
            self.field_infos = [
                function_field_info_factory(param) for param in parameters
            ]

    def lookup(self, lookup_key: Any) -> Optional[Any]:
        """ Type-safe limited usage wrapper around container.get"""
        return None

    def inject(self, lookup_key: Any) -> Optional[Any]:
        """Type-safe, replaceable wrapper around the injector """
        return None

    def __call__(self) -> Any:
        args = {}

        # Go through each field and apply policies
        for field_info in self.field_infos:
            field_name = field_info.field_name

            result: Optional[Result] = None
            for rule in RULES:
                r = rule(field_info, self)
                result: Result = r()

                # These results cause processing to break and stop
                # processing through any more rules.
                if isinstance(result, Found):
                    # This rule matched and found a result, assign and bail
                    break
                elif isinstance(result, Error):
                    # Something went horribly wrong, bail out not just
                    # of any more rules, but bail out completely of
                    # target construction, with a ValueError.
                    tn = self.target.__name__
                    prefix = f'{tn}|{field_name}|{rule.__name__}|{result.value.__name__}'
                    msg = f'{prefix}: {result.msg}'
                    raise ValueError(msg)
                elif isinstance(result, Init):
                    # The target is a dataclass and this field is
                    # marked as init=True, so no injection wanted.
                    break

            # All the rules for this field have run.
            if isinstance(result, Found):
                # This is kosher, put the value in the args.
                args[field_name] = result.value
            elif isinstance(result, Init):
                # This is ok, no need to put anything in the args.
                pass
            elif isinstance(result, NotFound):
                # Let's make a nice error message to remove some magic
                pass
            elif isinstance(result, Skip):
                # No rules provided a value, let's look at the field
                # field default and get it from there. In theory we could
                # skip this, but we want to detect a problem and raise a
                # very-specific, helpful error message.
                pass
            else:
                # We shouldn't get here. Every rule should return a
                # ``Result`` from the allowed list. Raise an error.
                pass

            # DON'T DO THIS! The Get operator now handles this. We will
            # delete this once the old injector tests have been moved
            # over and we can prove this isn't needed.
            # except FoundValueField as exc:
            #     this_value = exc.value
            #     if isclass(this_value):
            #         # This "service" is actually injectable, instead of
            #         # a plain factory. At the moment, we just have a class.
            #         # Use this injector instance to turn it into an instance.
            #         this_value = self(this_value)
            #     args[field_name] = this_value
            #     continue

        return self.target(**args)
