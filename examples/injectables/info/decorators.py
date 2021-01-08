from wired_injector import injectable

from .constants import Kind


class config(injectable):
    kind = Kind.config

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info = dict(shortname='bob')
