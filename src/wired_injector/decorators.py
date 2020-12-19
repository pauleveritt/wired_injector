from typing import TypeVar, Callable, Type, Optional

from venusian import Scanner, attach

protocol = TypeVar("protocol")


# TODO: This is all speculative from Glyph's approach
def adherent(
    c: Callable[[], protocol]
) -> Callable[[Type[protocol]], Type[protocol]]:  # pragma: no cover
    def decor(input_value: Type[protocol]) -> Type[protocol]:
        return input_value

    return decor


class injectable:
    """ ``venusian`` decorator to register an injectable factory  """

    for_ = None  # Give subclasses a chance to give default, e.g. view
    use_props = False

    def __init__(
        self,
        for_: type = None,
        context: Type = None,
        use_props: Optional[bool] = None,
    ):
        if for_ is not None:
            # Use passed in for_ value, otherwise, use the class attr
            self.for_ = for_
        self.context = context
        if use_props is not None:
            self.use_props = use_props

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
