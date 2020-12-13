from typing import TypeVar, Callable, Optional, Any, Type

from venusian import Scanner, attach
from wired import ServiceContainer, ServiceRegistry

protocol = TypeVar("protocol")


# TODO: This is all speculative from Glyph's approach
def adherent(
        c: Callable[[], protocol]
) -> Callable[[Type[protocol]], Type[protocol]]:  # pragma: no cover
    def decor(input_value: Type[protocol]) -> Type[protocol]:
        return input_value

    return decor


def register_injectable(
        registry: ServiceRegistry,
        for_: Callable,
        target: Callable = None,
        context: Optional[Any] = None,
):
    """ Imperative form of the injectable decorator """

    def injectable_factory(container: ServiceContainer):
        return target

    registry.register_factory(injectable_factory, for_, context=context)


class injectable:
    for_ = None  # Give subclasses a chance to give default, e.g. view

    def __init__(self, for_: type = None, context: Type = None):
        if for_ is not None:
            # Use passed in for_ value, otherwise, use the class attr
            self.for_ = for_
        self.context = context

    def __call__(self, wrapped):
        def callback(scanner: Scanner, name: str, cls):
            for_ = self.for_ if self.for_ else cls
            registry: ServiceRegistry = getattr(scanner, 'registry')

            register_injectable(
                registry,
                for_=for_,
                target=cls,
                context=self.context,
            )

        attach(wrapped, callback, category='wired')
        return wrapped
