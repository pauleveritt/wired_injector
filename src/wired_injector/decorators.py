from typing import TypeVar, Callable, Optional, Any, Type

from venusian import Scanner, attach
from wired import ServiceContainer, ServiceRegistry

protocol = TypeVar("protocol")


def adherent(c: Callable[[], protocol]) -> Callable[[Type[protocol]], Type[protocol]]:
    def decor(input_value: Type[protocol]) -> Type[protocol]:
        return input_value

    return decor


def register_component(
        registry: ServiceRegistry,
        for_: Callable,
        target: Callable = None,
        context: Optional[Any] = None
):
    """ Imperative form of the component decorator """

    def component_factory(container: ServiceContainer):
        return target if target else for_

    registry.register_factory(
        component_factory, for_, context=context
    )


class injectable:
    def __init__(self, for_: type = None, context: Type = None):
        self.for_ = for_
        self.context = context

    def __call__(self, wrapped):
        def callback(scanner: Scanner, name: str, cls):
            for_ = self.for_ if self.for_ else cls
            registry: ServiceRegistry = getattr(scanner, 'registry')

            register_component(
                registry,
                for_,
                target=cls,
                context=self.context,
            )

        attach(wrapped, callback, category='wired')
        return wrapped
