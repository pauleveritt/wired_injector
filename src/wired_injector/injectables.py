"""
Record then apply all the registrations.

Configurator-like system which can record all the injectables, apply them,
then report on them for uses such as generation of Sphinx config directives.

"""
from dataclasses import dataclass, field
from typing import Callable, Set, Optional, Any

from wired_injector import InjectorRegistry


@dataclass(frozen=True)
class Injectable:
    """
    All the info in ``register_injectable``
    """

    for_: Callable
    target: Optional[Callable]
    context: Optional[Any]
    use_props: bool
    area: Optional[str] = None
    phase: Optional[str] = None


@dataclass
class Injectables:
    registry: InjectorRegistry
    items: Set[Injectable] = field(default_factory=set)

    def add(self, injectable: Injectable):
        self.items.add(injectable)

    def find(
            self,
            area: Optional[str] = None,
            by_phase: Optional[bool] = False,
    ) -> Optional[Set[Injectable]]:
        if area is None:
            return self.items

        results = {
            injectable
            for injectable in self.items
            if injectable.area == area
        }

        if by_phase:
            results = set(sorted(results, key=lambda v: v.phase))
        return results
