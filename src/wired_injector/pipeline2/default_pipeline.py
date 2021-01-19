from dataclasses import dataclass
from typing import Any, Optional

from . import Container


@dataclass
class DefaultPipeline:
    """
    Bundled implementation of the Pipeline protocol.
    """

    container: Container
    target: Any

    def lookup(self, lookup_key: Any) -> Optional[Any]:
        """ Type-safe limited usage wrapper around container.get"""
        return None

    def inject(self, lookup_key: Any) -> Optional[Any]:
        """Type-safe, replaceable wrapper around the injector """
        return None
