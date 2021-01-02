from dataclasses import dataclass
from enum import Enum

import pytest
from wired_injector import InjectorRegistry
from wired_injector.injectables import Injectables, Injectable


class Area(Enum):
    system = 1
    app = 2
    plugins = 3
    site = 4


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


def test_find_area(full_injectables):
    results = full_injectables.find(area=Area.system)
    first = results[0]
    assert Phase.postinit == first.phase


def test_find_area_phase(full_injectables):
    results = full_injectables.find(area=Area.system, by_phase=True)
    first = results[0]
    assert Phase.init == first.phase


def test_apply_injectables(empty_injectables, system_init_one):
    empty_injectables.apply_injectable(system_init_one)
    container = empty_injectables.registry.create_injectable_container()
    result: DummyTarget = container.get(DummyTarget)
    assert 'Dummy Target' == result.title


@pytest.fixture
def system_init_one():
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
def app_init_one():
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
        system_init_one, system_postinit_one,
        app_init_one,
) -> Injectables:
    ir = InjectorRegistry()
    i = Injectables(ir)
    i.add(system_postinit_one)
    i.add(system_init_one)
    i.add(app_init_one)
    return i
