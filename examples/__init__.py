import sys
from types import ModuleType
from typing import Optional, Union

from venusian import Scanner
from wired import ServiceRegistry, ServiceContainer
from wired_injector import Injector

from . import factories
from .factories import View, Customer, FrenchCustomer, Greeting

PACKAGE = Optional[Union[ModuleType, str]]


def caller_module(level=2, sys=sys):
    module_globals = sys._getframe(level).f_globals
    module_name = module_globals.get('__name__') or '__main__'
    module = sys.modules[module_name]
    return module


def caller_package(level=2, caller_module=caller_module):
    # caller_module in arglist for tests
    module = caller_module(level + 1)
    f = getattr(module, '__file__', '')
    if ('__init__.py' in f) or ('__init__$py' in f):  # empty at >>>
        # Module is a package
        return module
    # Go up one level to get package
    package_name = module.__name__.rsplit('.', 1)[0]
    return sys.modules[package_name]


def example_registry(pkg: PACKAGE = None) -> ServiceRegistry:
    registry = ServiceRegistry()
    scanner = Scanner(registry=registry)
    scanner.scan(factories)

    # Now scan for custom factories
    if pkg is None:
        # Get the caller module and import it
        pkg = caller_package()
    elif isinstance(pkg, str):
        # importlib.resource package specification
        pkg = None
    scanner.scan(pkg)

    return registry


def example_container(some_registry) -> ServiceContainer:
    some_container = some_registry.create_container(context=Customer())
    injector = Injector(some_container)
    some_container.register_singleton(injector, Injector)
    return some_container


def example_french_container(some_registry) -> ServiceContainer:
    some_container = some_registry.create_container(
        context=FrenchCustomer()
    )
    injector = Injector(some_container)
    some_container.register_singleton(injector, Injector)
    return some_container
