from dataclasses import dataclass

from .protocols import Customer


@dataclass()
class RegularCustomer:
    first_name: str = 'Marie'


@dataclass()
class FrenchCustomer:
    first_name: str = 'Sophie'


@dataclass()
class RegularGreeter:
    salutation: str = 'Hello'

    def greet(self, customer: Customer) -> str:
        msg = f'{self.salutation} {customer.first_name}!'
        return msg


@dataclass()
class FrenchGreeter:
    salutation: str = 'Salut'

    def greet(self, customer: Customer) -> str:
        msg = f'{self.salutation} {customer.first_name}!'
        return msg
