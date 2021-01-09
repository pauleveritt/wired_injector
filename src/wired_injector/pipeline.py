from typing import Any, Tuple

from wired import ServiceContainer
from .operators import Operator


def process_pipeline(
    container: ServiceContainer,
    pipeline: Tuple[Operator, ...],
    start: Any,
    target,
):
    iter_pipeline = iter(pipeline)
    result = start
    while iter_pipeline:
        try:
            operator = next(iter_pipeline)
            result = operator(result, container, target)
        except StopIteration:
            return result
