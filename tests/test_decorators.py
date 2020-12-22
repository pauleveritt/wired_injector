"""

Test usage of wired and components via decorators instead of
imperative.

More cumbersome (due to scanner) to copy around so placed into a
single test.

"""

from dataclasses import dataclass

import pytest
from wired.dataclasses import register_dataclass
from wired_injector import injectable, Injector, InjectorRegistry
from wired_injector.operators import Attr, Context, Get

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


class FirstContext:
    def __init__(self):
        self.name = 'First Context'


class SecondContext:
    def __init__(self):
        self.name = 'Second Context'


class ThirdContext:
    def __init__(self):
        self.name = 'Third Context'


@dataclass
class Settings:
    greeting: str = 'Hello'


@injectable()
@dataclass
class Heading:
    person: str
    name: Annotated[str, Context(), Attr('name')]
    greeting: Annotated[str, Get(Settings), Attr('greeting')]


@injectable()
@dataclass
class URL:
    name: str = 'Some URL'

    def message(self):
        return self.name


@dataclass
class Config:
    """ An old-school, non-injectable factory """

    punctuation: str


@injectable()
@dataclass
class ScannableConfig:
    """ Injectable with no venusian scan category """

    punctuation: str = '!'


@injectable(category='config')
@dataclass
class ScannableConfig2:
    """ Provide a venusian scan category """

    punctuation: str = '!'


def config_factory(container):
    return Config(punctuation='!')


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


@injectable(for_=Heading, context=ThirdContext)
@dataclass
class ThirdHeading:
    """ Double injection but with a plain factory, not injectable """

    greeting: Annotated[str, Get(Settings), Attr('greeting')]
    config: Config  # Annotated[Config, Get(Config)]


@pytest.fixture
def registry() -> InjectorRegistry:
    registry = InjectorRegistry()
    registry.scan()
    register_dataclass(registry, Settings)
    return registry


def test_injectable_first(registry):
    context = FirstContext()
    container = registry.create_injectable_container(context=context)
    injector = container.get(Injector)
    props = dict(person='Some Person')
    # TODO Injector.__call__ typing has a challenge with positional
    #   vs. keyword-only, might need to re-think system props
    heading: Heading = injector(Heading, **props)  # type: ignore
    assert 'Some Person' == heading.person
    assert 'First Context' == heading.name
    assert 'Hello' == heading.greeting


def test_injectable_second(registry):
    context = SecondContext()
    container = registry.create_injectable_container(context=context)
    injector = container.get(Injector)
    props = dict(person='Another Person')
    # TODO Injector.__call__ typing has a challenge with positional
    #   vs. keyword-only, might need to re-think system props
    heading: Heading = injector(Heading, **props)  # type: ignore
    assert 'Another Person' == heading.person
    assert 'Second Context' == heading.name
    assert 'Hello' == heading.greeting


def test_injectable_double(registry):
    """ Ensure double injection works with both injectable and factory """

    registry.register_factory(config_factory, Config)
    container = registry.create_injectable_container()
    injector = container.get(Injector)
    heading: ThirdHeading = injector(ThirdHeading)
    assert 'Hello' == heading.greeting
    assert '!' == heading.config.punctuation


def test_injectable_scan_category_default():
    """ Use the decorator default for the venusian scan category """

    registry = InjectorRegistry()
    registry.scan()
    container = registry.create_injectable_container()
    config: ScannableConfig = container.get(ScannableConfig)
    assert '!' == config.punctuation


def test_injectable_scan_category_wired():
    """ Scan for the value of the default category (wired) """

    registry = InjectorRegistry()
    registry.scan(categories=('wired',))
    container = registry.create_injectable_container()
    config: Config = container.get(ScannableConfig)
    assert '!' == config.punctuation


def test_injectable_scan_category_custom():
    """ Provide a venusian scan category """

    registry = InjectorRegistry()
    registry.scan(categories=('config',))
    container = registry.create_injectable_container()
    config: ScannableConfig2 = container.get(ScannableConfig2)
    assert '!' == config.punctuation


def test_injectable_scan_category_not_found():
    """ Scan for something bogus and fail """

    registry = InjectorRegistry()
    registry.scan(categories=('BOGUS',))
    container = registry.create_injectable_container()
    with pytest.raises(LookupError):
        # Fails because this decorator registered under a
        # category not matching what we scanned for
        container.get(ScannableConfig2)
