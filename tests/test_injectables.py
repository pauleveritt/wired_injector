from dataclasses import dataclass
from enum import Enum

import pytest
from wired_injector import InjectorRegistry, injectable
from wired_injector.injectables import Injectables, Injectable


class Area(Enum):
    system = 1
    app = 2
    plugins = 3
    site = 4


class Phase(Enum):
    init = 1
    postinit = 2


class Kind(Enum):
    config = 1
    component = 2
    view = 3
    injectable = 4


@dataclass
class DummyTarget:
    title: str = 'Dummy Target'


@injectable()
@dataclass
class InjectableHeading:
    name: str = 'Injectable Heading'


def test_construction(empty_injectables):
    assert empty_injectables.items == []
    assert empty_injectables.pending_items == []


def test_add_injectable(empty_injectables, system_init_one):
    empty_injectables.add(system_init_one)
    first = empty_injectables.pending_items[0]
    assert SystemInitOne == first.target


def test_commit(empty_injectables, system_init_one):
    empty_injectables.add(system_init_one)
    empty_injectables.commit(Area.system)
    first = empty_injectables.items[0]
    assert Area.system == first.area


def test_find_all(full_injectables):
    results = full_injectables.find_by_area()
    assert len(results) == len(full_injectables.items)


def test_find_area(full_injectables, system_init_two):
    full_injectables.commit(area=Area.system)
    results = full_injectables.find_by_area(area=Area.system)
    first = results[0]
    assert system_init_two.info['title'] == first.info['title']


def test_find_area_phase(full_injectables):
    results = full_injectables.find_by_area(area=Area.system, by_phase=True)
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
    init_area_app = [
        i.info.get('title')
        for i in init[Area.app]
        if hasattr(i, 'info') and i.info is not None
    ]
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
    full_injectables.apply_injectables()
    container = full_injectables.registry.create_injectable_container()
    result = container.get(DummyTarget)
    assert result.__class__.__name__ == 'AppPostInitThree'


def test_injectable_registry_defer_true():
    # When using Injectables, regular calls to register_injectable
    # are not applied immediately. This is signalled through the
    # ``defer`` flag.
    @dataclass
    class Heading:
        name: str = 'Default Name'

    # First pass through, injectable not added to registry and
    # we don't commit/apply.
    registry = InjectorRegistry(use_injectables=True)
    registry.register_injectable(Heading)
    # No commit
    # No apply
    container = registry.create_injectable_container()
    with pytest.raises(LookupError):
        container.get(Heading)


def test_injectable_registry_commit_apply():
    # Use the imperative ``register_injectable`` to queue up some
    # registrations. Then commit them using an ``Area``. Apply
    # the registrations and do a lookup.
    @dataclass
    class Heading:
        name: str = 'Default Name'

    registry = InjectorRegistry(use_injectables=True)
    registry.register_injectable(Heading)
    registry.injectables.commit(area=Area.system)
    registry.injectables.apply_injectables()
    container = registry.create_injectable_container()
    heading: Heading = container.get(Heading)
    assert 'Default Name' == heading.name


def test_injectable_registry_decorators():
    # Use the decorator to do `register_injectable`.

    registry = InjectorRegistry(use_injectables=True)
    registry.scan()
    registry.injectables.commit(area=Area.system)
    registry.injectables.apply_injectables()
    container = registry.create_injectable_container()
    heading: InjectableHeading = container.get(InjectableHeading)
    assert 'Injectable Heading' == heading.name


def test_injectable_registry_multiple():
    # Multiple registrations usually obey "last registration wins."
    # With ``phases`` we can control the ordering.
    @dataclass
    class Heading:
        name: str = 'System Name'

    @dataclass
    class AppHeading:
        name: str = 'App Name'

    @dataclass
    class SiteHeading:
        name: str = 'Site Name'

    registry = InjectorRegistry(use_injectables=True)

    # Use phases to control the registration order. Even though this one is
    # registered first (and thus would be overridden later), it winds up
    # being used because it is in a later phase.
    registry.register_injectable(
        for_=Heading,
        target=SiteHeading,
        phase=Phase.postinit,
        info=dict(title='site heading'),
    )
    registry.register_injectable(
        for_=Heading,
        target=Heading,
        phase=Phase.init,
        info=dict(title='system heading'),
    )
    registry.register_injectable(
        for_=Heading,
        target=AppHeading,
        phase=Phase.init,
        info=dict(title='app heading'),
    )
    registry.injectables.commit(area=Area.system)
    registry.injectables.apply_injectables()
    container = registry.create_injectable_container()
    heading: Heading = container.get(Heading)
    assert heading.__class__.__name__ == 'SiteHeading'


def test_injectable_registry_areas():
    # Organize the universe into areas
    @dataclass
    class Heading:
        name: str = 'System Name'

    @dataclass
    class AppHeading:
        name: str = 'App Name'

    @dataclass
    class SiteHeading:
        name: str = 'Site Name'

    registry = InjectorRegistry(use_injectables=True)

    # Register for Area.site
    # Ordinarily we woudld do this last, but the order the areas
    # go in doesn't matter.
    registry.register_injectable(
        for_=Heading,
        target=SiteHeading,
        area=Area.site,
        info=dict(title='site heading'),
    )
    registry.injectables.commit(area=Area.site)

    # Register for Area.system
    registry.register_injectable(
        for_=Heading,
        target=Heading,
        area=Area.system,
        info=dict(title='system heading'),
    )
    registry.injectables.commit(area=Area.system)

    # Register for Area.app
    registry.register_injectable(
        for_=Heading,
        target=AppHeading,
        area=Area.app,
        info=dict(title='app heading'),
    )
    registry.injectables.commit(area=Area.app)

    # Now apply all the injectables
    registry.injectables.apply_injectables()
    container = registry.create_injectable_container()
    heading: Heading = container.get(Heading)
    assert heading.__class__.__name__ == 'SiteHeading'


def test_all_info(full_injectables):
    # Get any injectables that had an info structure

    results = full_injectables.get_info()
    assert len(results) == 9


def test_info_for_kind(full_injectables):
    # Get info for matching kind

    results = full_injectables.get_info(kind=Kind.config)
    assert len(results) == 4


@dataclass()
class SystemInitOne:
    title: str = 'System Init One'


@dataclass()
class SystemInitTwo:
    title: str = 'System Init Two'


@dataclass()
class SystemInitThree:
    title: str = 'System Init Three'


@dataclass()
class SystemPostInitOne:
    title: str = 'System PostInit One'


@dataclass()
class SystemPostInitTwo:
    title: str = 'System PostInit Two'


@dataclass()
class AppInitOne:
    title: str = 'App Init One'


@dataclass()
class SystemInitThree:
    title: str = 'System Init Three'


@dataclass()
class AppPostInitThree:
    title: str = 'App PostInit Three'


@dataclass()
class AppInitTwo:
    title: str = 'App Init Two'


@dataclass()
class AppInitThree:
    title: str = 'App Init Three'


@pytest.fixture
def system_init_one():
    return Injectable(
        for_=DummyTarget,
        target=SystemInitOne,
        context=None,
        use_props=False,
        area=None,
        phase=Phase.init,
        kind=Kind.config,
        info=dict(title='system_init_one'),
    )


@pytest.fixture
def system_init_two():
    return Injectable(
        for_=DummyTarget,
        target=SystemInitTwo,
        context=None,
        use_props=False,
        area=None,
        phase=Phase.init,
        kind=Kind.config,
        info=dict(title='system_init_two'),
    )


@pytest.fixture
def system_init_three():
    return Injectable(
        for_=DummyTarget,
        target=SystemInitThree,
        context=None,
        use_props=False,
        area=None,
        phase=Phase.init,
        kind=Kind.component,
        info=dict(title='system_init_three'),
    )


@pytest.fixture
def system_postinit_one():
    return Injectable(
        for_=DummyTarget,
        target=SystemPostInitOne,
        context=None,
        use_props=False,
        area=None,
        phase=Phase.postinit,
        kind=Kind.component,
        info=dict(title='system_postinit_one'),
    )


@pytest.fixture
def system_postinit_two():
    return Injectable(
        for_=DummyTarget,
        target=SystemPostInitTwo,
        context=None,
        use_props=False,
        area=None,
        phase=Phase.postinit,
        kind=Kind.view,
        info=dict(title='system_postinit_two'),
    )


@pytest.fixture
def system_postinit_three():
    return Injectable(
        for_=DummyTarget,
        target=SystemInitThree,
        context=None,
        use_props=False,
        area=None,
        phase=Phase.postinit,
        kind=Kind.view,
    )


@pytest.fixture
def app_init_one():
    return Injectable(
        for_=DummyTarget,
        target=AppInitOne,
        context=None,
        use_props=False,
        area=None,
        phase=Phase.init,
        kind=Kind.config,
        info=dict(title='app_init_one'),
    )


@pytest.fixture
def app_postinit_three():
    return Injectable(
        for_=DummyTarget,
        target=AppPostInitThree,
        context=None,
        use_props=False,
        area=None,
        phase=Phase.postinit,
        kind=Kind.view,
        info=dict(title='app_init_one'),
    )


@pytest.fixture
def app_init_two():
    return Injectable(
        for_=DummyTarget,
        target=AppInitTwo,
        context=None,
        use_props=False,
        area=None,
        phase=Phase.init,
        kind=Kind.component,
        info=dict(title='app_init_two'),
    )


@pytest.fixture
def app_init_three():
    return Injectable(
        for_=DummyTarget,
        target=AppInitThree,
        context=None,
        use_props=False,
        area=Area.app,
        phase=Phase.init,
        kind=Kind.config,
        info=dict(title='app_init_three'),
    )


@pytest.fixture
def empty_injectables() -> Injectables:
    ir = InjectorRegistry(use_injectables=True)
    i = Injectables(ir)
    return i


@pytest.fixture
def full_injectables(
    system_init_one,
    system_init_two,
    system_init_three,
    system_postinit_one,
    system_postinit_two,
    system_postinit_three,
    app_init_one,
    app_init_two,
    app_init_three,
    app_postinit_three,
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
    i.add(app_postinit_three)
    i.commit(Area.app)
    return i
