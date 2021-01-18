from dataclasses import dataclass
from typing import Any

from . import Container


@dataclass
class DefaultPipeline:
    """
    Bundled implementation of the Pipeline protocol.
    """

    container: Container
    target: Any
