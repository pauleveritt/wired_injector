from typing import Protocol


class Customer(Protocol):
    first_name: str


class Greeter(Protocol):
    salutation: str

    def greet(self, customer: Customer) -> str:
        ...
