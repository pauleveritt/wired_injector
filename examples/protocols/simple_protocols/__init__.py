"""
Solution: Use protocols.

Works in Python. Static analysis: ok in PyCharm and mypy.

- Replace base classes with protocols
- Use `Tuple[Customer, ...]` to connect instances to protocol
- Put type hint on greeters, as PyCharm gets mad without it
  * Show this
- mypy then kicks in

- Introduce protocol errors
  - RegularCustomer.first_name as int
  - FrenchGreeter.greet from Customer -> FrenchCustomer
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
    # Oops: The pain!! Time for some Any
    greeters: Mapping[Customer, Greeter] = {
        RegularCustomer: RegularGreeter(),
        FrenchCustomer: FrenchGreeter(),
    }
    for customer in customers:
        greeter = greeters[customer.__class__]
        greeting = greeter.greet(customer)
        greetings.append(greeting)

    expected = ['Hello Marie!', 'Salut Sophie!']
    return expected, greetings
