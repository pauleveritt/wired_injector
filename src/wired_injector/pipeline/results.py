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


@dataclass
class Error:
    """
    Problems that can't be skipped for something downstream.

    Some situations, like failing a container lookup, can be passed
    over with ``NotFound`` for something later to try and handle.
    Others, such as trying to do a lookup with a string, are flat-out
    mistakes and processing should stop. No more operators, no more
    rules being processed.
    """

    msg: Optional[str]
    value: Type[Any]


@dataclass
class Init:
    """
    The field is not part of the args collected for construction.

    Dataclasses have a concept of field(init=False) which means this
    field is neither part of the passed-in args nor a default value.
    The field is assigned in ``__post_init__``.
    """

    value: Type[Any]
    msg: Optional[str] = None


@dataclass
class Skip:
    """
    The rule didn't match its conditions so go on to the next rule.

    Each rule has some conditions: the service container rule expects
    the field type to be ServiceContainer, the pipeline rule expects
    a non-empty sequence after ``Annotated``. When these aren't
    met, the rule can use this ``Result`` to explicitly flag "Continue
    on to the next thing."
    """

    value: Type[Any]
    msg: Optional[str] = None
