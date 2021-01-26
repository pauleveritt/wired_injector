"""
Solve problems with base ``Customer``.

Nouns are a reasonable usage of superclasses for (nominal)
typing. But (haha) even this has some problems.
"""

from dataclasses import dataclass
from typing import Tuple


class Customer:
    first_name: str


@dataclass()
class RegularCustomer(Customer):
    first_name: str = 'Marie'


@dataclass()
class FrenchCustomer(Customer):
    first_name: str = 'Sophie'


@dataclass()
class Greeter:
    salutation: str = 'Hello'

    def greet(self, customer: Customer) -> str:
        msg = f'{self.salutation} {customer.first_name}!'
        return msg


def test() -> Tuple[Tuple[str, str], Tuple[str, str]]:
    regular_customer = RegularCustomer()
    greeter = Greeter()
    greeting1 = greeter.greet(regular_customer)
    french_customer = FrenchCustomer()
    greeting2 = greeter.greet(french_customer)

    expected = ('Hello Marie!', 'Hello Sophie!')
    return expected, (greeting1, greeting2)
