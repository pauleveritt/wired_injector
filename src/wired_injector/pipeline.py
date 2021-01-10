from dataclasses import dataclass
from typing import Any

from wired import ServiceContainer
from wired_injector.field_info import FieldInfo


@dataclass
class Pipeline:
    field_info: FieldInfo
    container: ServiceContainer
    start: Any
    target: Any

    def __call__(self):
        operators = self.field_info.operators
        iter_pipeline = iter(operators)
        result = self.start
        while iter_pipeline:
            try:
                operator = next(iter_pipeline)
                result = operator(result, self.container, self.target)
            except StopIteration:
                return result
