from enum import Enum
from importlib import import_module
from types import ModuleType
from typing import Optional, Union, Callable, Any, Mapping, Tuple

from venusian import Scanner
from wired import ServiceRegistry, ServiceContainer
from wired_injector import Injector
from zope.interface import Interface

from .utils import caller_package

PACKAGE = Optional[Union[ModuleType, str]]


class InjectorContainer(ServiceContainer):
    """A service container that can inject with props.

    We need a separate ``inject`` method that can take keyword
    args and use as "props" during injection. These props then
    supersede other values used for a field.
    """

    def inject(
            self,
            iface_or_type=Interface,
            *,
            cget_props: Optional[Mapping[str, Any]] = None,
            system_props: Optional[Mapping[str, Any]] = None,
            **kwargs,
    ):
        """ Same as container.get but with props, via injector """

        # cget_props is a way to prevent container.get keywords, such as
        # context/name/default, from getting trampled on by regular props.
        # If "the system" wants those passed into the underlying .get(),
        # then put them in cget_props.
        if cget_props is None:
            cget_props = {}

        # TODO If your component has a prop of 'name' or 'context'
        # then those will collide with the .get args of same name.
        klass = self.get(
            iface_or_type,
            context=cget_props.get('context', None),
            name=cget_props.get('name', ''),
            default=cget_props.get('default', None),
        )
        injector = self.get(Injector)
        result = injector(klass, system_props, **kwargs)
        return result


class InjectorRegistry(ServiceRegistry):
    """ A registry with a venusian Scanner and injector"""

    scanner: Scanner

    def __init__(
            self,
            factory_registry=None,
            use_injectables: bool = False,
    ):
        super().__init__(factory_registry=factory_registry)
        self.scanner = Scanner(registry=self)
        from .injectables import Injectables

        if use_injectables:
            self.injectables = Injectables(registry=self)
        else:
            self.injectables = None

    def scan(self,
             pkg: PACKAGE = None,
             categories: Tuple[str, ...] = None,
             ):
        if pkg is None:
            # Get the caller module and import it
            pkg = caller_package()
        elif isinstance(pkg, str):
            # importlib.resource package specification
            pkg = import_module(pkg)
        self.scanner.scan(pkg, categories=categories)

    def create_container(self, *, context=None) -> InjectorContainer:
        return InjectorContainer(self._factories, context=context)

    def create_injectable_container(
            self, *, context=None
    ) -> InjectorContainer:
        container = self.create_container(context=context)
        injector = Injector(container)
        container.register_singleton(injector, Injector)
        return container

    def register_injectable(
            self,
            for_: Callable,
            target: Optional[Callable] = None,
            context: Optional[Any] = None,
            use_props: bool = False,
            area: Optional[Enum] = None,
            phase: Optional[Enum] = None,
            info: Optional[Mapping[Any, Any]] = None,
            defer: bool = True,
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
            area: Which area such as ``Area.system`` currently in
            phase: Which phase such as ``Phase.init`` currently in
            info: Extra info a particular ``Kind`` might want such as ``config.shortname``
            defer: The flag that signifies Injectables is applying the injectables.
        """

        # To avoid doing:
        #   registry.register_injectable(Heading, Heading)
        # ...allow target to be optional. In that case, assign
        # target to equal for_.
        if target is None:
            target = for_

        def injectable_factory(container: ServiceContainer):
            if use_props:
                # Just return the target, it will be
                # constructed when the props are available
                return target
            else:
                injector = container.get(Injector)
                instance = injector(target)
                return instance

        setattr(target, '__wired_factory__', injectable_factory)

        if self.injectables is None:
            # self.injectables is None means we aren't using Injectables
            # so immediately register.
            self.register_factory(target, for_, context=context)
        elif not defer:
            # defer is False when injectables comes back later and
            #   does ``apply_injectables``
            self.register_factory(target, for_, context=context)
        else:
            # If using Injectables, defer the registration until later.
            # Doing import here because of (surprise) circular import.
            from .injectables import Injectable
            injectable = Injectable(
                for_=for_,
                target=target,
                context=context,
                use_props=use_props,
                area=area,
                phase=phase,
                info=info,
            )
            self.injectables.add(injectable)
