"""

Test usage of wired and components via decorators instead of
imperative.

More cumbersome (due to scanner) to copy around so placed into a
single test.

"""
from dataclasses import dataclass

import pytest
from wired import ServiceRegistry
from wired.dataclasses import factory, register_dataclass
from wired_injector import injectable, Injector
from wired_injector.operators import Attr, Context, Get

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


class FirstContext:
    def __init__(self):
        self.name = 'First Context'


class SecondContext:
    def __init__(self):
        self.name = 'Second Context'


@factory()
@dataclass
class Settings:
    greeting: str = 'Hello'


@injectable()
@dataclass
class Heading:
    person: str
    name: Annotated[str, Context(), Attr('name')]
    greeting: Annotated[str, Get(Settings), Attr('greeting')]


@pytest.fixture
def registry() -> ServiceRegistry:
    import sys
    from venusian import Scanner

    registry = ServiceRegistry()
    scanner = Scanner(registry=registry)
    current_module = sys.modules[__name__]
    scanner.scan(current_module)
    register_dataclass(registry, Settings)
    return registry


@injectable()
@dataclass
class URL:
    name: str = 'Some URL'


@injectable()
@dataclass
class ShowURL:
    url: URL


@injectable(for_=Heading, context=SecondContext)
@dataclass
class SecondHeading:
    person: str
    name: Annotated[str, Context(), Attr('name')]
    greeting: Annotated[str, Get(Settings), Attr('greeting')]


def test_injectable_first(registry):
    context = FirstContext()
    container = registry.create_container(context=context)
    injector = Injector(container)
    props = dict(person='Some Person')
    heading: Heading = injector(Heading, **props)
    assert 'Some Person' == heading.person
    assert 'First Context' == heading.name
    assert 'Hello' == heading.greeting


def test_injectable_second(registry):
    context = SecondContext()
    container = registry.create_container(context=context)
    injector = Injector(container)
    props = dict(person='Another Person')
    heading: Heading = injector(Heading, **props)
    assert 'Another Person' == heading.person
    assert 'Second Context' == heading.name
    assert 'Hello' == heading.greeting


def test_injectable_url(registry):
    """ Ensure double injection works """
    container = registry.create_container()
    injector = Injector(container)
    show_url: ShowURL = injector(ShowURL)
    assert 'Some URL' == show_url.url.name
