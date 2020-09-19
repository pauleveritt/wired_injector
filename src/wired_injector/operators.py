from dataclasses import dataclass
from typing import Type, Any

from wired import ServiceContainer


# TODO This should be a Protocol but the typechecker then says a usage
#   in an annotation should be a generic.
class Operator:
    """ Part of a pipeline for field construction """

    def __call__(self, previous: Type, container: ServiceContainer) -> Any:
        ...


@dataclass(frozen=True)
class Get(Operator):
    __slots__ = ('lookup_type',)
    lookup_type: Type

    def __call__(self, previous: Type, container: ServiceContainer):
        return self.lookup_type
