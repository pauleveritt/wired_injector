"""
Record then apply all the registrations.

Configurator-like system which can record all the injectables, apply them,
then report on them for uses such as generation of Sphinx config directives.
"""
from dataclasses import dataclass, field, replace
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
    kind: Optional[Enum] = None
    phase: Optional[Enum] = None
    info: Optional[Mapping[Any, Any]] = None


GroupedInjectablesT = Dict[Enum, Dict[Enum, List[Injectable]]]


@dataclass(frozen=True)
class SortedValue:
    """
    Used to sort on enum values if present

    ``target_attribute`` will be ``phase`` or ``area``.
    """

    __slots__ = ['target_attribute']

    target_attribute: str

    def __call__(self, injectable: Injectable):
        """
        Return the target attribute from the injectable or None.

        This is used for sorting during grouping.
        """
        a = getattr(injectable, self.target_attribute)
        if a is None:
            # There are no phases/areas etc. on this value, so
            # just sort on 0
            return 0

        # Get the enum's value
        return getattr(a, 'value')


@dataclass
class Injectables:
    registry: InjectorRegistry
    items: List[Injectable] = field(default_factory=list)
    pending_items: List[Injectable] = field(default_factory=list)

    def add(self, injectable: Injectable):
        """ Queue up an injectable for later handling """
        self.pending_items.append(injectable)

    def commit(self, area: Enum):
        """ Move all pending, changing their area along the way """

        # Make sure to preserve order
        for injectable in self.pending_items:
            new_injectable = replace(injectable, area=area)
            self.items.append(new_injectable)

        # Now reset the pending_items
        self.pending_items.clear()

    def find_by_area(
        self,
        area: Optional[Enum] = None,
        by_phase: Optional[bool] = False,
    ) -> Optional[List[Injectable]]:
        """ Return the results by area, optionally sorted by phase """
        if area is None:
            if by_phase is not None:
                results = sorted(self.items, key=SortedValue('phase'))
                return results

            return self.items

        results = [
            injectable for injectable in self.items if injectable.area == area
        ]

        if by_phase:
            results = sorted(results, key=SortedValue('phase'))
        return results

    def get_grouped_injectables(self) -> GroupedInjectablesT:
        """ Grouped and sorted by area then phase """

        # Remember, Python 3.7+ orders dicts, allowing us to collect
        # entries in the order we will then process them
        results: Dict[Any, Any] = {}

        sorted_phases = sorted(self.items, key=SortedValue('phase'))
        for k1, phase in groupby(sorted_phases, key=lambda v: v.phase):
            results[k1] = {}
            # Reverse the sort, so higher-priority are registered last.
            sorted_areas = sorted(phase, key=SortedValue('area'))
            for k2, area in groupby(sorted_areas, key=lambda v: v.area):
                results[k1][k2] = []
                for injectable in list(area):
                    results[k1][k2].append(injectable)
        return results

    def apply_injectables(
        self,
        grouped_injectables: Optional[GroupedInjectablesT] = None,
    ):
        """ Apply the injectables in groups """

        if grouped_injectables is None:
            grouped_injectables = self.get_grouped_injectables()

        # Process in order of: phase, then area
        for phase in grouped_injectables.values():
            for area in phase.values():
                for injectable in area:
                    self.registry.register_injectable(
                        injectable.for_,
                        injectable.target,
                        context=injectable.context,
                        use_props=injectable.use_props,
                        defer=False,
                    )

    def get_info(self, kind: Optional[Enum] = None):
        """ Return injectables that have attached info."""

        results: List[Injectable] = [
            injectable
            for injectable in self.items
            if injectable.info is not None
        ]

        # If filtering by kind, do so
        if kind is not None:
            results = [
                injectable for injectable in results if injectable.kind == kind
            ]

        return results
