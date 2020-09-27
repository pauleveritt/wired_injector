from dataclasses import dataclass
from typing import Type, Any, Tuple

from wired import ServiceContainer

# TODO This should be a Protocol but the typechecker then says a usage
#   in an annotation should be a generic.


class Operator:
    """ Part of a pipeline for field construction """

    def __call__(self, previous: Any, container: ServiceContainer) -> Any:
        ...


@dataclass(frozen=True)
class Get(Operator):
    __slots__ = ('lookup_type',)
    lookup_type: Type

    def __call__(self, previous: Type, container: ServiceContainer):
        try:
            return container.get(self.lookup_type)
        except LookupError:
            # We don't want to just crash with a LookupError, as the
            # field might have a default. Thus, bail out of processing
            # the pipeline.
            from wired_injector.injector import SkipField
            raise SkipField()


@dataclass(frozen=True)
class Attr(Operator):
    __slots__ = ('lookup_type',)
    name: str

    def __call__(self, previous: Any, container: ServiceContainer):
        return getattr(previous, self.name)


def process_pipeline(
        container: ServiceContainer,
        pipeline: Tuple[Operator, ...],
        start: Type,
):
    iter_pipeline = iter(pipeline)
    result = start
    while iter_pipeline:
        try:
            operator = next(iter_pipeline)
            result = operator(result, container)
        except StopIteration:
            return result
