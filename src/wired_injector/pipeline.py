from dataclasses import dataclass
from typing import Any

from wired import ServiceContainer


@dataclass
class Pipeline:
    container: ServiceContainer
    start: Any
    target: Any

    def __call__(self, *args):
        iter_pipeline = iter(args)
        result = self.start
        while iter_pipeline:
            try:
                operator = next(iter_pipeline)
                result = operator(result, self.container, self.target)
            except StopIteration:
                return result
