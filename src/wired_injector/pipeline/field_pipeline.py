"""
Process all operators and result in a value, or handle the problem.

"""

from typing import Sequence

from . import (
    Operator,
    Result,
    Pipeline,
)
from .results import Error, Skip


def process_field_pipeline(
    operators: Sequence[Operator],
    pipeline: Pipeline,
) -> Result:
    """ Process each operator in the pipeline and return the result """

    iter_operators = iter(operators)
    # Get the first operator
    try:
        result = next(iter_operators)(None, pipeline)
    except StopIteration:
        # This means the pipeline was empty, so Skip.
        return Skip(value=Pipeline)

    # If this is an error, don't process any more operators
    if isinstance(result, Error):
        return result

    # Proceed with remaining operators
    while iter_operators:
        try:
            operator = next(iter_operators)
            result = operator(result, pipeline)

            # If this is an error, don't process any more operators
            if isinstance(result, Error):
                return result
        except StopIteration:
            return result

    return result  # pragma: no cover
