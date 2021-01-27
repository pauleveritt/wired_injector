from dataclasses import dataclass
from typing import Tuple


@dataclass()
class Customer:
    first_name: str = 'Marie'


@dataclass()
class Greeter:
    salutation: str = 'Hello'

    def greet(self, customer: Customer) -> str:
        msg = f'{self.salutation} {customer.first_name}!'
        return msg


def test() -> Tuple[str, str]:
    customer = Customer()
    greeter = Greeter()
    greeting = greeter.greet(customer)

    expected = 'Hello Marie!'
    return expected, greeting
