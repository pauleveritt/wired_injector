from typing import TypeVar, Callable, Type

from venusian import Scanner, attach

protocol = TypeVar("protocol")


# TODO: This is all speculative from Glyph's approach
def adherent(
        c: Callable[[], protocol]
) -> Callable[[Type[protocol]], Type[protocol]]:  # pragma: no cover
    def decor(input_value: Type[protocol]) -> Type[protocol]:
        return input_value

    return decor


#
# def register_injectable(
#         registry: ServiceRegistry,
#         for_: Callable,
#         target: Callable = None,
#         context: Optional[Any] = None,
# ):
#     """Imperative form of the injectable decorator.
#
#     This can be called imperatively instead of using the
#     ``@injectable`` decorator. In fact, the decorator just
#     calls this function.
#
#     Args:
#         registry: The registry to use for this.
#         for_: A for
#         target: A target
#         context: A context
#     """
#
#     def injectable_factory(container: ServiceContainer):
#         return target
#
#     registry.register_factory(injectable_factory, for_, context=context)
#

class injectable:
    """ ``venusian`` decorator to register an injectable factory  """

    for_ = None  # Give subclasses a chance to give default, e.g. view
    use_props = False

    def __init__(self, for_: type = None, context: Type = None):
        if for_ is not None:
            # Use passed in for_ value, otherwise, use the class attr
            self.for_ = for_
        self.context = context

    def __call__(self, wrapped):
        def callback(scanner: Scanner, name: str, cls):
            for_ = self.for_ if self.for_ else cls
            registry = getattr(scanner, 'registry')
            registry.register_injectable(
                for_=for_,
                target=cls,
                context=self.context,
                use_props=self.use_props,
            )

        attach(wrapped, callback, category='wired')
        return wrapped
