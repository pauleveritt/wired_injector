"""
Result classes to hold value that signify certain outcomes.

From a flow-of-control perspective, an operator/rule needs to signal to
the caller the decision it reached. We could use exceptions, but
those have some anti-patterns regarding typing and are hard to
reason about.

Instead, an operator or rule should always return a result object. This
object holds the value but also indicates the status, so the caller
can then do the right thing in the rest of the operator pipeline.
"""
from dataclasses import dataclass
from typing import Any, Type, Optional


@dataclass
class Found:
    """ Operation was looked up in the container and found """

    value: Any
    msg: Optional[str] = None


@dataclass
class NotFound:
    """
    A lookup was done in the container but nothing matched.

    In this case the value assigned is the operator/rule class
    that failed and the msg is the text to display. The caller
    will then make further decisions about the exception value
    to raise.
    """

    msg: Optional[str]
    value: Type[Any]
