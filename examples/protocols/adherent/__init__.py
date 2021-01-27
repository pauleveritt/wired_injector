"""
Get warnings if the implementation doesn't conform to protocol.

Works in Python. Static analysis: ok in PyCharm and fails mypy.

- Add usage of the `@adherent` decorator from Glyph
- Asserts that the following "implements" a protocol
- Works in mypy (no-op in PyCharm)
"""

from typing import Tuple, Mapping, List

from .models import (
    FrenchCustomer,
    FrenchGreeter,
    RegularCustomer,
    RegularGreeter,
)
from .protocols import Customer, Greeter


def test() -> Tuple[List[str], List[str]]:
    customers: Tuple[Customer, ...] = (
        RegularCustomer(), FrenchCustomer(),
    )
    greetings = []
    greeters: Mapping[str, Greeter] = dict(
        RegularCustomer=RegularGreeter(),
        FrenchCustomer=FrenchGreeter(),
    )
    for customer in customers:
        greeter = greeters[customer.__class__.__name__]
        greeting = greeter.greet(customer)
        greetings.append(greeting)

    expected = ['Hello Marie!', 'Salut Sophie!']
    return expected, greetings
