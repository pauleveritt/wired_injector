from dataclasses import dataclass

from wired_injector import injectable


@injectable()
@dataclass
class View:
    name: str = 'View'
