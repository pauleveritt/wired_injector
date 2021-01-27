from typing import Protocol


class Customer(Protocol):
    first_name: str


class View(Protocol):
    customer: Customer
    punctuation: str
    salutation: str

    def __call__(self) -> str:
        pass
