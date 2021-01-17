"""
Implementations of major operators such as ``Get``.
"""
from dataclasses import dataclass
from typing import Any, Optional

from . import OperatorResult, Pipeline
from .operator_results import Found, NotFound


@dataclass
class Get:
    lookup_key: Any
    attr: Optional[str] = None

    def __call__(
        self,
        previous: Optional[Any],
        pipeline: Pipeline,
    ) -> OperatorResult:
        value = pipeline.lookup(self.lookup_key)
        if value is None:
            # This lookup type isn't in the
            nf = NotFound(value=self.lookup_key)
            return nf
        f = Found(value=value)
        return f
