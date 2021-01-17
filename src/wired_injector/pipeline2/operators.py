"""
Implementations of major operators such as ``Get``.
"""
from dataclasses import dataclass
from typing import Any, Optional

from . import OperatorResult, Pipeline
from .operator_results import Found


@dataclass
class Get:
    lookup_type: Any
    attr: Optional[str] = None

    def __call__(
        self,
        previous: Optional[Any],
        pipeline: Pipeline,
    ) -> OperatorResult:
        value = pipeline.lookup(self.lookup_type)
        f = Found(value=value)
        return f
