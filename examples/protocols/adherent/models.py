from dataclasses import dataclass

from wired_injector.decorators import adherent

from .protocols import Customer, Greeter


@adherent(Customer)
@dataclass()
class RegularCustomer:
    first_name: str = 'Marie'


@adherent(Customer)
@dataclass()
class FrenchCustomer:
    first_name: str = 'Sophie'


@adherent(Greeter)
@dataclass()
class RegularGreeter:
    salutation: str = 'Hello'

    def greet(self, customer: Customer) -> str:
        msg = f'{self.salutation} {customer.first_name}!'
        return msg


@adherent(Greeter)
@dataclass()
class FrenchGreeter:
    salutation: str = 'Salut'

    def greet(self, customer: Customer) -> str:
        msg = f'{self.salutation} {customer.first_name}!'
        return msg
