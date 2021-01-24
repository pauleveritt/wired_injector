from enum import Enum

from wired_injector import injectable

from examples.factories import Customer


class Area(Enum):
    system = 1
    app = 2
    plugins = 3
    site = 4


def test_default():
    i = injectable(        for_=Customer    )
    assert i.for_ == Customer
    assert i.info is None
    assert i.kind is None
    assert i.phase is None
    assert i.use_props is False


def test_construction():
    # Yeh, there's a little "shut up the coverage" going on here
    i = injectable(
        for_=Customer,
        info={},
        kind=Area.system,
        phase=Area.system,
        use_props=True,
    )
    assert i.for_ == Customer
    assert i.info == {}
    assert i.kind == Area.system
    assert i.phase == Area.system
    assert i.use_props is True
