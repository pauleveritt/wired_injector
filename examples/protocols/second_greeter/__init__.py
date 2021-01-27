from dataclasses import dataclass
from typing import Tuple, List


class Customer:
    first_name: str


@dataclass()
class RegularCustomer(Customer):
    first_name: str = 'Marie'


@dataclass()
class FrenchCustomer(Customer):
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


def test() -> Tuple[List[str], List[str]]:
    customers = (RegularCustomer(), FrenchCustomer())
    greetings = []
    for customer in customers:
        if isinstance(customer, FrenchCustomer):
            greeter = FrenchGreeter()  # Oops: mypy fails
        else:
            greeter = RegularGreeter()
        greeting = greeter.greet(customer)
        greetings.append(greeting)

    expected = ['Hello Marie!', 'Salut Sophie!']
    return expected, greetings
