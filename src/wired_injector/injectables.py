"""
Record then apply all the registrations.

Configurator-like system which can record all the injectables, apply them,
then report on them for uses such as generation of Sphinx config directives.

"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional, Any, List

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
    area: Optional[Enum] = None
    phase: Optional[Enum] = None


@dataclass
class Injectables:
    registry: InjectorRegistry
    items: List[Injectable] = field(default_factory=list)

    def add(self, injectable: Injectable):
        self.items.append(injectable)

    def find(
            self,
            area: Optional[Enum] = None,
            by_phase: Optional[bool] = False,
    ) -> Optional[List[Injectable]]:
        if area is None:
            return self.items

        results = [
            injectable
            for injectable in self.items
            if injectable.area == area
        ]

        if by_phase:
            results = sorted(results, key=lambda v: v.phase.value)
        return results

    def apply_injectable(self, injectable: Injectable):
        self.registry.register_injectable(
            for_=injectable.for_,
            target=injectable.target,
            context=injectable.context,
            use_props=injectable.use_props,
        )

    def apply_injectables(self, areas: Enum, phases: Enum):
        """ Apply the injectables in groups """

        pass