import os
import sys

import pytest
from wired import ServiceContainer
from wired_injector import Injector

from examples import example_registry
from examples.factories import (
    Customer,
    FrenchCustomer,
)

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


@pytest.fixture
def this_registry():
    return example_registry()


@pytest.fixture
def regular_container(this_registry) -> ServiceContainer:
    c = this_registry.create_container(context=Customer())
    injector = Injector(c)
    c.register_singleton(injector, Injector)
    return c


@pytest.fixture
def french_container(this_registry) -> ServiceContainer:
    c = this_registry.create_container(context=FrenchCustomer())
    injector = Injector(c)
    c.register_singleton(injector, Injector)
    return c


@pytest.fixture
def regular_injector(regular_container):
    i: Injector = regular_container.get(Injector)
    return i


@pytest.fixture
def french_injector(french_container):
    i: Injector = french_container.get(Injector)
    return i


@pytest.fixture(scope="session", autouse=True)
def examples_path():
    """ Automatically add the root of the repo to path """
    ep = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
    sys.path.insert(0, ep)
