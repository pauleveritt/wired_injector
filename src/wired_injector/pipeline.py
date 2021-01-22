from dataclasses import dataclass
from typing import Any

from wired import ServiceContainer
from wired_injector.pipeline2 import FieldInfo


@dataclass
class Pipeline:
    field_info: FieldInfo
    container: ServiceContainer
    target: Any

    def __call__(self):
        operators = self.field_info.operators
        iter_pipeline = iter(operators)
        result = None
        while iter_pipeline:
            try:
                operator = next(iter_pipeline)
                result = operator(result, self)
            except StopIteration:
                return result
