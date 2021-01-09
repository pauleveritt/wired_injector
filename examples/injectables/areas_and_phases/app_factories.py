from dataclasses import dataclass

from wired_injector import injectable

from .system_factories import Settings

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore # noqa: F401


@injectable(for_=Settings)
@dataclass
class AppSettings:
    site_name: str = 'App Site'
