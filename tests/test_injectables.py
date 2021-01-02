import pytest
from wired_injector import InjectorRegistry
from wired_injector.injectables import Injectables, Injectable


class DummyTarget:
    pass


def test_construction(empty_injectables):
    assert empty_injectables.items == set()


def test_add_injectable(full_injectables):
    first = full_injectables.items.pop()
    assert DummyTarget == first.for_


def test_find_all(full_injectables):
    results = full_injectables.find()
    assert list(results) == list(full_injectables.items)


def test_find_area(full_injectables):
    results = full_injectables.find(area='system')
    first = list(results)[0]
    assert 'postinit' == first.phase


def test_find_area_phase(full_injectables):
    results = full_injectables.find(area='system', by_phase=True)
    first = list(results)[0]
    assert 'init' == first.phase


@pytest.fixture
def system_init_one():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=DummyTarget,
        use_props=False, area='system', phase='init',
    )


@pytest.fixture
def system_postinit():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=DummyTarget,
        use_props=False, area='system', phase='postinit',
    )


@pytest.fixture
def app_init_one():
    return Injectable(
        for_=DummyTarget, target=DummyTarget, context=DummyTarget,
        use_props=False, area='app', phase='init',
    )


@pytest.fixture
def empty_injectables() -> Injectables:
    ir = InjectorRegistry()
    i = Injectables(ir)
    return i


@pytest.fixture
def full_injectables(
        system_init_one, system_postinit,
        app_init_one,
) -> Injectables:
    ir = InjectorRegistry()
    i = Injectables(ir)
    i.add(system_postinit)
    i.add(system_init_one)
    i.add(app_init_one)
    return i
