"""
Record then apply all the registrations.

Configurator-like system which can record all the injectables, apply them,
then report on them for uses such as generation of Sphinx config directives.

"""
from dataclasses import dataclass, field
from enum import Enum
from itertools import groupby
from typing import Callable, Optional, Any, List, Type

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

    def get_grouped_injectables(self):
        """ Grouped and sorted by area then phase """

        results = {}
        sorted_areas = sorted(self.items, key=lambda v: v.area.value)
        for k1, area in groupby(sorted_areas, key=lambda v: v.area):
            results[k1] = {}
            sorted_phases = sorted(area, key=lambda v: v.phase.value)
            for k2, phase in groupby(sorted_phases, key=lambda v: v.phase):
                results[k1][k2] = []
                for injectable in phase:
                    results[k1][k2].append(injectable)
        return results

    def apply_injectables(
            self,
            grouped_injectables,
    ):
        """ Apply the injectables in groups """

        pass
