from dataclasses import dataclass

from wired_injector import injectable

from examples.protocols.pluggable_system.app.protocols import Customer, View


@injectable(for_=View)
@dataclass
class SiteAmericanView:
    customer: Customer
    punctuation: str = '!'
    salutation: str = 'HOWDY'

    def __call__(self) -> str:
        fn = self.customer.first_name
        # Add a space before punctuation
        msg = f'{self.salutation} {fn} {self.punctuation}'
        return msg
