"""
Process all operators and result in a value, or handle the problem.

"""

from typing import Iterator

from . import Operator, Result, Pipeline


def process_field_pipeline(
    operators: Iterator[Operator],
    pipeline: Pipeline,
) -> Result:
    """ Process each operator in the pipeline and return the result """

    # Get the first one
    result = next(operators)(None, pipeline)
    while operators:
        try:
            operator = next(operators)
            result = operator(result, pipeline)
        except StopIteration:
            return result

    return result
