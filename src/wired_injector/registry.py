from importlib import import_module
from types import ModuleType
from typing import Optional, Union, Callable, Any

from venusian import Scanner
from wired import ServiceRegistry, ServiceContainer
from wired_injector import Injector
from wired_injector.utils import caller_package

PACKAGE = Optional[Union[ModuleType, str]]


class InjectorRegistry(ServiceRegistry):
    """ A registry with a venusian Scanner and injector"""

    scanner: Scanner

    def __init__(self, factory_registry=None):
        super().__init__(factory_registry=factory_registry)
        self.scanner = Scanner(registry=self)

    def scan(self, pkg: PACKAGE = None):
        if pkg is None:
            # Get the caller module and import it
            pkg = caller_package()
        elif isinstance(pkg, str):
            # importlib.resource package specification
            pkg = import_module(pkg)
        self.scanner.scan(pkg)

    def create_injectable_container(self, *, context=None) -> ServiceContainer:
        container = self.create_container(context=context)
        injector = Injector(container)
        container.register_singleton(injector, Injector)
        return container

    def register_injectable(
            self,
            for_: Callable,
            target: Callable = None,
            context: Optional[Any] = None,
            use_props: bool = False,
    ):
        """Imperative form of the injectable decorator.

        This can be called imperatively instead of using the
        ``@injectable`` decorator. In fact, the decorator just
        calls this function.

        Args:
            for_: The type or interface to register for
            target: A callable or class to register
            context: A container context
            use_props: This factory should be injected with keyword args
        """

        def injectable_factory(container: ServiceContainer):
            if use_props:
                # Just return the target, it will be
                # constructed when the props are available
                return target
            else:
                injector = container.get(Injector)
                instance = injector(target)
                return instance

        target.__wired_factory__ = injectable_factory
        self.register_factory(target, for_, context=context)
