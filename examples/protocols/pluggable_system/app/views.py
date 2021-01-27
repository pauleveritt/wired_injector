from dataclasses import dataclass

from wired_injector import injectable

from .models import FrenchCustomer
from examples.protocols.pluggable_system.app.protocols import Customer, View


@injectable(for_=View)
@dataclass
class AmericanView:
    customer: Customer
    punctuation: str = '!'
    salutation: str = 'Hello'

    def __call__(self) -> str:
        fn = self.customer.first_name
        msg = f'{self.salutation} {fn}{self.punctuation}'
        return msg


@injectable(for_=View, context=FrenchCustomer)
@dataclass
class FrenchView:
    customer: Customer
    punctuation: str = '.'
    salutation: str = 'Bonjour'

    def __call__(self) -> str:
        fn = self.customer.first_name
        msg = f'{self.salutation} {fn}{self.punctuation}'
        return msg
