from dataclasses import dataclass
from typing import Tuple


@dataclass()
class RegularCustomer:
    first_name: str = 'Marie'


@dataclass()
class FrenchCustomer:
    first_name: str = 'Sophie'


@dataclass()
class Greeter:
    salutation: str = 'Hello'

    def greet(self, customer: RegularCustomer) -> str:
        msg = f'{self.salutation} {customer.first_name}!'
        return msg


def test() -> Tuple[Tuple[str, str], Tuple[str, str]]:
    regular_customer = RegularCustomer()
    greeter = Greeter()
    greeting1 = greeter.greet(regular_customer)
    french_customer = FrenchCustomer()
    greeting2 = greeter.greet(french_customer)  # Oops

    expected = ('Hello Marie!', 'Hello Sophie!')
    return expected, (greeting1, greeting2)
