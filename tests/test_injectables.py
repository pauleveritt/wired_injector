from dataclasses import dataclass
from enum import Enum

import pytest
from wired_injector import InjectorRegistry
from wired_injector.injectables import Injectables, Injectable

"""

NEXT
- Change items to be a dict of:

dict(
    Area.system = dict(
        Kind.config = dict(
            Phase.init = [
                injectable,
                injectable

"""


class Area(Enum):
    system = 1
    app = 2
    plugins = 3
    site = 4


class Kind(Enum):
    config = 1
    component = 2
    view = 3
    injectable = 4


class Phase(Enum):
    init = 1
    postinit = 2


@dataclass
class DummyTarget:
    title: str = 'Dummy Target'


def test_construction(empty_injectables):
    assert empty_injectables.items == []


def test_add_injectable(full_injectables):
    first = full_injectables.items[0]
    assert DummyTarget == first.for_


def test_find_all(full_injectables):
    results = full_injectables.find()
    assert results == full_injectables.items


def test_find_area(full_injectables, system_init_two):
    results = full_injectables.find(area=Area.system)
    first = results[0]
    assert system_init_two == first


def test_find_area_phase(full_injectables):
    results = full_injectables.find(area=Area.system, by_phase=True)
    first = results[0]
    assert Phase.init == first.phase


def test_apply_injectable(empty_injectables, system_init_one):
    empty_injectables.apply_injectable(system_init_one)
    container = empty_injectables.registry.create_injectable_container()
    result: DummyTarget = container.get(DummyTarget)
    assert 'Dummy Target' == result.title


#
# def test_foo():
#     people = (
#         dict(name='D', age=20),
#         dict(name='A', age=21),
#         dict(name='E', age=22),
#         dict(name='F', age=18),
#         dict(name='B', age=17),
#         dict(name='A', age=16),
#         dict(name='D', age=30),
#     )
#     sorted_people = sorted(people, key=lambda v: v['name'])
#     results = {}
#     for k, grouped_people in groupby(sorted_people, key=lambda v: v['name']):
#         results[k] = []
#         for person in grouped_people:
#             results[k].append(person)
#
#     assert 9 == results.keys()


def test_get_grouped_injectables(full_injectables):
    results = full_injectables.get_grouped_injectables()
    assert [Area.system, Area.app] == list(results.keys())

    # System
    system = results[Area.system]
    assert [Phase.init, Phase.postinit] == list(system.keys())
    system_values = list(system.values())
    assert 2 == len(system_values)
    # assert 9 == [i.]

    # App
    app = results[Area.app]
    assert [Phase.init, ] == list(app.keys())
    app_values = list(app.values())
    assert 1 == len(app_values)

    # container = full_injectables.registry.create_injectable_container()
    # result: DummyTarget = container.get(DummyTarget)
    # assert 'Dummy Target' == result.title


@pytest.fixture
def system_init_one():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.system, phase=Phase.init,
    )


@pytest.fixture
def system_init_two():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.system, phase=Phase.init,
    )


@pytest.fixture
def system_init_three():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.system, phase=Phase.init,
    )


@pytest.fixture
def system_postinit_one():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.system, phase=Phase.postinit,
    )


@pytest.fixture
def system_postinit_two():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.system, phase=Phase.postinit,
    )


@pytest.fixture
def system_postinit_three():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.system, phase=Phase.postinit,
    )


@pytest.fixture
def app_init_one():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.app, phase=Phase.init,
    )


@pytest.fixture
def app_init_two():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.app, phase=Phase.init,
    )


@pytest.fixture
def app_init_three():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.app, phase=Phase.init,
    )


@pytest.fixture
def empty_injectables() -> Injectables:
    ir = InjectorRegistry()
    i = Injectables(ir)
    return i


@pytest.fixture
def full_injectables(
        system_init_one, system_init_two, system_init_three,
        system_postinit_one, system_postinit_two, system_postinit_three,
        app_init_one, app_init_two, app_init_three,
) -> Injectables:
    ir = InjectorRegistry()
    i = Injectables(ir)
    i.add(system_init_two)
    i.add(system_postinit_two)
    i.add(app_init_three)
    i.add(system_postinit_one)
    i.add(system_init_one)
    i.add(app_init_one)
    i.add(system_init_three)
    i.add(system_postinit_three)
    i.add(app_init_two)
    return i
