from dataclasses import dataclass

from wired_injector import injectable

from .system_factories import Settings

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


@injectable(for_=Settings)
@dataclass
class SomePluginSettings:
    site_name: str = 'Some Plugin Site'
