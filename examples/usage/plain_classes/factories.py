from wired_injector import injectable


# Site settings
@injectable()
class Settings:
    site_name: str

    def __init__(self, site_name: str = 'My Site'):
        self.site_name = site_name


# View that uses site settings
@injectable()
class View:
    settings: Settings

    def __init__(self, my_settings: Settings):
        # Note that the *name* of the argument doesn't matter,
        # the injector is looking at the type.
        self.settings = my_settings

    @property
    def name(self):
        site_name = self.settings.site_name
        return f'View - {site_name}'
