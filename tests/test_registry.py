from dataclasses import dataclass

from wired_injector import InjectorRegistry


class DummyScan:
    def __init__(self):
        self.called_with = None

    def __call__(self, pkg):
        self.called_with = pkg


def test_injector_registry_construction():
    registry = InjectorRegistry()
    assert hasattr(registry, 'scanner')
    assert hasattr(registry, 'scan')


def test_injector_container_get():
    # Use .get and the wired factory that is stamped on the callable
    @dataclass
    class Heading:
        name: str = 'Default Name'

    registry = InjectorRegistry()
    registry.register_injectable(Heading, use_props=True)
    container = registry.create_injectable_container()
    heading: Heading = container.get(Heading)
    assert 'Default Name' == heading.name


def test_injector_container_inject_props():
    # Instead of using .get, use .inject to pass props
    @dataclass
    class Heading:
        first_name: str = 'Default Name'

    registry = InjectorRegistry()
    registry.register_injectable(Heading, use_props=True)
    container = registry.create_injectable_container()
    heading: Heading = container.inject(
        Heading, first_name='Injected Name'
    )
    assert 'Injected Name' == heading.first_name


def test_injector_container_inject_name_prop():
    # Injecting a prop of ``name`` collides with the usage of
    # container.get(iface, name=)
    @dataclass
    class Heading:
        name: str = 'Default Name'

    registry = InjectorRegistry()
    registry.register_injectable(Heading, use_props=True)
    container = registry.create_injectable_container()
    heading: Heading = container.inject(
        Heading, name='Injected Name'
    )
    assert 'Injected Name' == heading.name


def test_injector_registry_scan_caller():
    registry = InjectorRegistry()
    ds = DummyScan()
    registry.scanner.scan = ds
    registry.scan()
    assert 'tests' == ds.called_with.__name__  # type: ignore


def test_injector_registry_scan_pkg():
    from examples import index

    registry = InjectorRegistry()
    ds = DummyScan()
    registry.scanner.scan = ds
    registry.scan(index)
    assert 'examples.index' == ds.called_with.__name__  # type: ignore


def test_injector_registry_scan_string():
    registry = InjectorRegistry()
    ds = DummyScan()
    registry.scanner.scan = ds
    registry.scan('examples.index')
    assert 'examples.index' == ds.called_with.__name__  # type: ignore


def test_injector_target_none():
    # The target argument is optional and defaults to None
    @dataclass
    class Heading:
        name: str = 'Default Name'

    registry = InjectorRegistry()
    registry.register_injectable(Heading, use_props=True)
    container = registry.create_injectable_container()
    heading: Heading = container.get(Heading)
    assert 'Default Name' == heading.name
