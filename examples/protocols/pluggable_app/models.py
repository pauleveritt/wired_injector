from dataclasses import dataclass


@dataclass
class AmericanCustomer:
    first_name: str = 'Marie'


@dataclass
class FrenchCustomer:
    first_name: str = 'Sophie'
