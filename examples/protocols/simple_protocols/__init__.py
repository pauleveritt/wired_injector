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
        # Oops: PyCharm doesn't like this without the above
        greeter = greeters[customer.__class__]
        greeting = greeter.greet(customer)
        greetings.append(greeting)

    expected = ['Hello Marie!', 'Salut Sophie!']
    return expected, greetings
