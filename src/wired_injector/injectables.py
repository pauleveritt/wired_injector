"""
Record then apply all the registrations.

Configurator-like system which can record all the injectables, apply them,
then report on them for uses such as generation of Sphinx config directives.

- `register_injectable` (and thus `@injectable` and all derived decorators)
  defer their registration until a second `apply_injectables` step
- Group the injectables by phase, then "area" (e.g. system, app, plugin,
  site), then apply them
- Keep track of the injectables to allow instrospection and other special
  uses, such as generating Sphinx config directives from the
  `kind=Kind.config` injectables
- The actual area/phase/kind vocabularies are external, provided as enums,
  which allow sorting the priority of the values
- Generic `info` dict which lets a system pass along extra information that
  can be put to some use
- Rely on Python 3.7 or later ordering of dicts
"""
from dataclasses import dataclass, field
from enum import Enum
from itertools import groupby
from typing import Callable, Optional, Any, List, Mapping, Dict

from wired_injector import InjectorRegistry


@dataclass(frozen=True)
class Injectable:
    """
    All the info in ``register_injectable``
    """

    for_: Callable = field(repr=False)
    target: Optional[Callable] = field(repr=False)
    context: Optional[Any] = field(repr=False)
    use_props: bool = field(repr=False)
    area: Optional[Enum] = None
    phase: Optional[Enum] = None
    info: Optional[Mapping[Any, Any]] = None


GroupedInjectablesT = Dict[Enum, Dict[Enum, List[Injectable]]]


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

        # Remember, Python 3.7+ orders dicts, allowing us to collect
        # entries in the order we will then process them
        results: GroupedInjectablesT = {}
        sorted_phases = sorted(self.items, key=lambda v: v.phase.value)
        for k1, phase in groupby(sorted_phases, key=lambda v: v.phase):
            results[k1] = {}
            sorted_areas = sorted(phase, key=lambda v: v.area.value)
            for k2, area in groupby(sorted_areas, key=lambda v: v.area):
                results[k1][k2] = []
                for injectable in area:
                    results[k1][k2].append(injectable)
        return results

    def apply_injectables(
            self,
            grouped_injectables,
    ):
        """ Apply the injectables in groups """

        # Process in order of: phase, then area
        for phase in grouped_injectables.values():
            for area in phase.values():
                for injectable in area:
                    self.registry.register_injectable(
                        for_=injectable.for_,
                        target=injectable.target,
                        context=injectable.context,
                        use_props=injectable.use_props,
                    )
