from dataclasses import dataclass

from wired_injector import injectable


@dataclass
class View:
    view_name: str = 'View'


class view(injectable):
    for_ = View
    use_props = True


@view()
@dataclass
class CustomView:
    view_name: str = 'Custom View'
