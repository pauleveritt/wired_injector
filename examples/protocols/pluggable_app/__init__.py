from typing import Tuple

from .app import main
from .models import FrenchCustomer


def test() -> Tuple[str, str]:
    customer = FrenchCustomer()
    result = main(customer=customer)

    expected = 'Bonjour Sophie.'
    return result, expected
