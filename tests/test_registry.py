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


def test_injector_registry_scan_caller():
    registry = InjectorRegistry()
    ds = DummyScan()
    registry.scanner.scan = ds
    registry.scan()
    assert 'tests' == ds.called_with.__name__


def test_injector_registry_scan_pkg():
    from examples import index
    registry = InjectorRegistry()
    ds = DummyScan()
    registry.scanner.scan = ds
    registry.scan(index)
    assert 'examples.index' == ds.called_with.__name__


def test_injector_registry_scan_string():
    registry = InjectorRegistry()
    ds = DummyScan()
    registry.scanner.scan = ds
    registry.scan('examples.index')
    assert 'examples.index' == ds.called_with.__name__
