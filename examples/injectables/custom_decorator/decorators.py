from wired_injector import injectable

from .constants import Phase


class config(injectable):
    phase = Phase.init
