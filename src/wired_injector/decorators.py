from enum import Enum
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
    phase: Optional[Enum] = None
    use_props = False
    category = 'wired'  # venusian scan category

    def __init__(
            self,
            for_: type = None,
            category: Optional[str] = None,
            context: Optional[Type] = None,
            phase: Optional[Enum] = None,
            use_props: Optional[bool] = None,
    ):
        if for_ is not None:
            # Use passed in value, otherwise, use the class attr
            self.for_ = for_
        if category is not None:
            # Use passed in value, otherwise, use the class attr
            self.category = category
        self.context = context
        if phase is not None:
            # Use passed in value, otherwise, use the class attr
            self.phase = phase
        if use_props is not None:
            # Use passed in value, otherwise, use the class attr
            self.use_props = use_props

    def __call__(self, wrapped):
        def callback(scanner: Scanner, name: str, cls):
            for_ = self.for_ if self.for_ else cls
            registry = getattr(scanner, 'registry')
            registry.register_injectable(
                for_=for_,
                target=cls,
                context=self.context,
                phase=self.phase,
                use_props=self.use_props,
            )

        attach(wrapped, callback, category=self.category)
        return wrapped
