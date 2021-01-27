from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from wired import service_factory, ServiceContainer
from wired_injector import injectable
from wired_injector.pipeline.operators import Get

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore # noqa: F401


# Normal kind of customer
@dataclass
class Customer:
    name: Optional[str] = 'Customer'


# Default View
@service_factory()
@dataclass
class View:
    name: Optional[str] = 'View'

    def __call__(self) -> Optional[str]:
        return self.name

    @property
    def caps_name(self) -> Optional[str]:
        return self.name.upper() if self.name is not None else None

    @classmethod
    def __wired_factory__(cls, container: ServiceContainer) -> View:
        return cls()


# Example of an injectable factory
@injectable()
@dataclass
class Greeting:
    customer_name: Annotated[str, Get(View, attr='caps_name')]

    def __call__(self) -> str:
        return f'Hello {self.customer_name}'


# Special kind of Customer
@dataclass
class FrenchCustomer(Customer):
    name: Optional[str] = 'French Customer'


# Special kind of View, for that special kind of Customer
@service_factory(for_=View, context=FrenchCustomer)
@dataclass
class FrenchView(View):
    name: Optional[str] = 'French View'

    @classmethod
    def __wired_factory__(cls, container: ServiceContainer) -> FrenchView:
        return cls()
