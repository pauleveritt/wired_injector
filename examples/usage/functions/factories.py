from typing import NamedTuple

from wired_injector import injectable


# Site settings
@injectable()
class Settings(NamedTuple):
    site_name: str = 'My Site'


# View that uses site settings
@injectable()
def View(settings: Settings):
    site_name = settings.site_name
    name = f'View - {site_name}'
    return dict(name=name)
