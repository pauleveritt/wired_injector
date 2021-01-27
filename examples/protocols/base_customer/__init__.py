from dataclasses import dataclass
from typing import Tuple


class Customer:
    first_name: str


@dataclass()
class AmericanCustomer(Customer):
    first_name: str = 'Judy'


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
    regular_customer = AmericanCustomer()
    greeter = Greeter()
    greeting1 = greeter.greet(regular_customer)
    french_customer = FrenchCustomer()
    greeting2 = greeter.greet(french_customer)

    expected = ('Hello Judy!', 'Hello Sophie!')
    return expected, (greeting1, greeting2)
