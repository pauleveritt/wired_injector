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


@dataclass
class DummyTarget2:
    title: str = 'Dummy Target2'


def test_construction(empty_injectables):
    assert empty_injectables.items == []
    assert empty_injectables.pending_items == []


def test_add_injectable(empty_injectables, system_init_one):
    empty_injectables.add(system_init_one)
    first = empty_injectables.pending_items[0]
    assert DummyTarget == first.for_


def test_commit(empty_injectables, system_init_one):
    empty_injectables.add(system_init_one)
    empty_injectables.commit(Area.system)
    first = empty_injectables.items[0]
    assert Area.system == first.area


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


def test_get_grouped_injectables(full_injectables):
    results = full_injectables.get_grouped_injectables()
    assert [Phase.init, Phase.postinit] == list(results.keys())

    # Init -> System, App
    init = results[Phase.init]
    assert [Area.system, Area.app] == list(init.keys())
    init_values = list(init.values())
    assert 2 == len(init_values)
    init_area_system = [i.info['title'] for i in init[Area.system]]
    expected = ['system_init_two', 'system_init_one', 'system_init_three']
    assert expected == init_area_system
    init_area_app = [i.info['title'] for i in init[Area.app]]
    expected = ['app_init_three', 'app_init_one', 'app_init_two']
    assert expected == init_area_app

    # Postinit -> System, App
    postinit = results[Phase.postinit]
    assert [Area.system, Area.app] == list(postinit.keys())
    postinit_values = list(init.values())
    assert 2 == len(postinit_values)
    postinit_area_system = [i.info['title'] for i in postinit[Area.app]]
    expected = ['app_init_one']
    assert expected == postinit_area_system
    postinit_area_app = [i.info['title'] for i in postinit[Area.app]]
    assert expected == postinit_area_app


def test_apply_injectables_all(full_injectables):
    results = full_injectables.get_grouped_injectables()
    full_injectables.apply_injectables(results)
    container = full_injectables.registry.create_injectable_container()
    result: DummyTarget2 = container.get(DummyTarget)
    assert isinstance(result, DummyTarget2)


def test_apply_injectables_by_area(full_injectables):
    results = full_injectables.get_grouped_injectables()
    full_injectables.apply_injectables(results)
    container = full_injectables.registry.create_injectable_container()
    result: DummyTarget2 = container.get(DummyTarget)
    assert isinstance(result, DummyTarget2)


@pytest.fixture
def system_init_one():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.system, phase=Phase.init,
        info=dict(title='system_init_one'),
    )


@pytest.fixture
def system_init_two():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.system, phase=Phase.init,
        info=dict(title='system_init_two'),
    )


@pytest.fixture
def system_init_three():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.system, phase=Phase.init,
        info=dict(title='system_init_three'),
    )


@pytest.fixture
def system_postinit_one():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.system, phase=Phase.postinit,
        info=dict(title='system_postinit_one'),
    )


@pytest.fixture
def system_postinit_two():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.system, phase=Phase.postinit,
        info=dict(title='system_postinit_two'),
    )


@pytest.fixture
def system_postinit_three():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.system, phase=Phase.postinit,
        info=dict(title='system_postinit_three'),
    )


@pytest.fixture
def app_init_one():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.app, phase=Phase.init,
        info=dict(title='app_init_one'),
    )


@pytest.fixture
def app_postinit_last():
    # This is the last registration, should override all the others.
    # Let's signify that registering it for a different target.
    return Injectable(
        for_=DummyTarget, target=DummyTarget2, context=None,
        use_props=False, area=Area.app, phase=Phase.postinit,
        info=dict(title='app_init_one'),
    )


@pytest.fixture
def app_init_two():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.app, phase=Phase.init,
        info=dict(title='app_init_two'),
    )


@pytest.fixture
def app_init_three():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=None,
        use_props=False, area=Area.app, phase=Phase.init,
        info=dict(title='app_init_three'),
    )


@pytest.fixture
def empty_injectables() -> Injectables:
    ir = InjectorRegistry(use_injectables=True)
    i = Injectables(ir)
    return i


@pytest.fixture
def full_injectables(
        system_init_one, system_init_two, system_init_three,
        system_postinit_one, system_postinit_two, system_postinit_three,
        app_init_one, app_init_two, app_init_three, app_postinit_last,
) -> Injectables:
    ir = InjectorRegistry(use_injectables=True)
    i = Injectables(ir)
    i.add(system_init_two)
    i.commit(Area.system)
    i.add(system_postinit_two)
    i.commit(Area.system)
    i.add(app_init_three)
    i.commit(Area.app)
    i.add(system_postinit_one)
    i.commit(Area.system)
    i.add(system_init_one)
    i.commit(Area.system)
    i.add(app_init_one)
    i.commit(Area.app)
    i.add(system_init_three)
    i.commit(Area.system)
    i.add(system_postinit_three)
    i.commit(Area.system)
    i.add(app_init_two)
    i.commit(Area.app)
    i.add(app_postinit_last)
    i.commit(Area.app)
    return i
