"""
Process all operators and result in a value, or handle the problem.

"""

from typing import Iterator

from . import Operator, Result, Pipeline
from .results import Error


def process_field_pipeline(
    operators: Iterator[Operator],
    pipeline: Pipeline,
) -> Result:
    """ Process each operator in the pipeline and return the result """

    # Get the first operator
    try:
        result = next(operators)(None, pipeline)
    except StopIteration:
        # This means the pipeline was empty,which is an error
        msg = f'Annotated was used with no subsequent operators'
        return Error(msg=msg, value=Operator)

    # If this is an error, don't process any more operators
    if isinstance(result, Error):
        return result

    # Proceed with remaining operators
    while operators:
        try:
            operator = next(operators)
            result = operator(result, pipeline)

            # If this is an error, don't process any more operators
            if isinstance(result, Error):
                return result
        except StopIteration:
            return result

    return result  # pragma: no cover
