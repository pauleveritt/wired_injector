"""
Record then apply all the registrations.

Configurator-like system which can record all the injectables, apply them,
then report on them for uses such as generation of Sphinx config directives.

A system based on ``Injectables`` works in 4 phases:

Find
====

Go look in the system, the app, plugins, and the site for injectables
that want to be registered.

Record
======

Instead of directly calling ``registry.register_factory``, record the
registration info into ``Injectables.pending_items``.

Commit
======

When finished with each area, e.g. ``system``, "commit" the
``pending_items`` with the enum value of the area, e.g. ``system``.
This does nothing more than:

- Remove each ``Injectable`` in ``pending_items``

- Change its ``area`` field from ``None`` to the value being committed

- Append it to the permanent ``items`` list

Apply
=====

After all the injectables have been collected, iterate through each,
in "order", and call ``InjectorRegistry.register_factory``.

What is the "order"? For each "phase" (in order), then each "area"
(in order). Thus, the system might register all ``phase=init`` injectables
first, and with those, ``area=system`` first. It's possible that, later,
a third level grouping is implemented, to allow register ``kind=config``
before other kinds of injectables.

The ``area`` is something under the control of the caller. We don't
demand that each usage of a decorator/register_injectable says whether
it is in the system, the app, or a plugin. That info can be determined
by the caller.

The ``phase``, though, *is* something each decorator/register_injectable
should determine. Only it knows if the information it is providing or
consuming should be at a certain point in registration. This is simplified
by a reasonable default: you can go first and don't depend on anything else.

- ``register_injectable`` (and thus ``@injectable`` and all derived decorators)
  defer their registration until a second ``apply_injectables`` step
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
            if by_phase:
                results = sorted(self.items, key=lambda v: v.phase.value)
                return results

            return self.items

        results = [
            injectable
            for injectable in self.items
            if injectable.area == area
        ]

        if by_phase:
            results = sorted(results, key=lambda v: v.phase.value)
        return results

    def get_grouped_injectables(self) -> GroupedInjectablesT:
        """ Grouped and sorted by area then phase """

        # Remember, Python 3.7+ orders dicts, allowing us to collect
        # entries in the order we will then process them
        results: GroupedInjectablesT = {}

        # Reverse the sort, so higher-priority are registered last.
        sorted_phases = sorted(self.items, key=SortedValue('phase'), reverse=True)
        for k1, phase in groupby(sorted_phases, key=lambda v: v.phase):
            results[k1] = {}
            # Reverse the sort, so higher-priority are registered last.
            sorted_areas = sorted(phase, key=SortedValue('area'), reverse=True)
            for k2, area in groupby(sorted_areas, key=lambda v: v.area):
                results[k1][k2] = []
                # Reverse the sort, so higher-priority are registered last.
                for injectable in reversed(list(area)):
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
