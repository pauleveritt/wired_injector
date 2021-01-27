from typing import Tuple

from .app import main
from .app.models import AmericanCustomer


def test() -> Tuple[str, str]:
    customer = AmericanCustomer()
    result = main(customer=customer)

    # The site overrode the view and added a space
    expected = 'HOWDY Marie !'
    return result, expected
