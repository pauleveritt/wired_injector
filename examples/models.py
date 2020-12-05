from dataclasses import dataclass
from typing import Optional

from wired_injector.operators import Get

try:
    from typing import Annotated
    from typing import Protocol
except ImportError:
    from typing_extensions import Annotated  # type: ignore
    from typing_extensions import Protocol  # type: ignore


@dataclass
class Customer:
    name: Optional[str] = 'Customer'


@dataclass
class FrenchCustomer(Customer):
    name: Optional[str] = 'French Customer'


@dataclass
class View:
    name: Optional[str] = 'View'

    def __call__(self):
        return self.name

    @property
    def caps_name(self):
        return self.name.upper()


@dataclass
class FrenchView(View):
    name: Optional[str] = 'French View'


def view_factory(container):
    return View()


def french_view_factory(container):
    return FrenchView()


@dataclass
class Greeting:
    customer_name: Annotated[str, Get(View, attr='caps_name')]

    def __call__(self):
        return f'Hello {self.customer_name}'
