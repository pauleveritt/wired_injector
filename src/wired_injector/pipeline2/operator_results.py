"""
OperatorResult classes to hold value that signify certain outcomes.

From a flow-of-control perspective, an operator needs to signal to
the caller the decision it reached. We could use exceptions, but
those have some anti-patterns regarding typing and are hard to
reason about.

Instead, an operator should always return a result object. This
object holds the value but also indicates the status, so the caller
can then do the right thing in the rest of the operator pipeline.
"""
from dataclasses import dataclass
from typing import Any, Type


@dataclass
class Found:
    """ Operation was looked up in the container and found """

    value: Any


@dataclass
class NotFound:
    """
    A lookup was done in the container but nothing matched.

    In this case the value assigned is the type/protocol that was
    being looked up. The caller will decide how to display that
    in an exception value.
    """

    value: Type[Any]
