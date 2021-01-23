from dataclasses import dataclass

from wired_injector import injectable
from wired_injector.pipeline.operators import Context, Attr

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore # noqa: F401


@dataclass
class Customer:
    name: str = 'Fred'


@dataclass
class FrenchCustomer:
    name: str = 'Marie'


@injectable()
@dataclass
class View:
    customer_name: Annotated[
        str,
        Context(),
        Attr('name'),
    ]

    @property
    def name(self):
        return f'Hello {self.customer_name}'


@injectable(for_=View, context=FrenchCustomer)
@dataclass
class FrenchView:
    customer_name: Annotated[
        str,
        Context(),
        Attr('name'),
    ]

    @property
    def name(self):
        return f'Bonjour {self.customer_name}'
