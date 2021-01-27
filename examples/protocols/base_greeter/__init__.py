from dataclasses import dataclass
from typing import List, Tuple


class Customer:
    first_name: str


@dataclass()
class RegularCustomer(Customer):
    first_name: str = 'Marie'


@dataclass()
class FrenchCustomer(Customer):
    first_name: str = 'Sophie'


class Greeter:
    salutation: str

    def greet(self, customer: Customer) -> str:
        msg = f'{self.salutation} {customer.first_name}!'
        return msg


@dataclass()
class RegularGreeter(Greeter):
    salutation: str = 'Hello'


@dataclass()
class FrenchGreeter(Greeter):
    salutation: str = 'Salut'


def test() -> Tuple[List[str], List[str]]:
    customers = (RegularCustomer(), FrenchCustomer())
    greetings = []
    for customer in customers:
        if isinstance(customer, FrenchCustomer):
            greeter: Greeter = FrenchGreeter()  # Oops: mypy made me do it
        else:
            greeter = RegularGreeter()
        greeting = greeter.greet(customer)
        greetings.append(greeting)

    expected = ['Hello Marie!', 'Salut Sophie!']
    return expected, greetings