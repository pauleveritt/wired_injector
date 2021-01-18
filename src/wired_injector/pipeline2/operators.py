"""
Implementations of major operators such as ``Get``.
"""
from dataclasses import dataclass
from inspect import isclass
from typing import Any, Optional

from . import Result, Pipeline
from .results import Found, NotFound


@dataclass(frozen=True)
class Get:
    """ Which service in the container to get """

    lookup_key: Any
    attr: Optional[str] = None

    def __call__(
        self,
        previous: Optional[Any],
        pipeline: Pipeline,
    ) -> Result:

        # Can't lookup a string, ever, so bail on this with an error.
        pass

        # Try to get an instance (or a class, if it is injectable)
        value = pipeline.lookup(self.lookup_key)
        if value is None:
            lookup_name = self.lookup_key.__name__
            msg = f"No service '{lookup_name}' found in container"
            nf = NotFound(msg=msg, value=Get)
            return nf

        if isclass(value):
            # We asked the container to get something and got back a
            # class instead of an instance. That means we are doing
            # *injection* so construct an injectable instance.
            value = pipeline.inject(value)

        # Are we plucking an attr?
        if self.attr is not None:
            value = getattr(value, self.attr)

        f = Found(value=value)
        return f


@dataclass(frozen=True)
class Attr:
    """ Pluck an attribute off the object coming in """

    name: str

    def __call__(
        self,
        previous: Any,
        pipeline: Pipeline,
    ) -> Result:
        value = getattr(previous, self.name)
        return Found(value=value)


@dataclass(frozen=True)
class Context:
    """ Get the current container's context object. """

    attr: Optional[str] = None

    def __call__(
        self,
        previous: Any,
        pipeline: Pipeline,
    ) -> Result:

        # If the container.context is None, then getting an
        # attr off of it is pointless. Bail out with NotFound
        # and let downstream try to get a field default.
        context = pipeline.container.context
        # TODO Result
        # if context is None:
        #     return NotFound
        value = pipeline.container.context
        if self.attr is not None:
            if value is not None:
                v = getattr(value, self.attr)
                value = Found(value=v)
            else:
                # Asking for an attr when the container.context
                # is None is an error, perhaps this field has a
                # default.
                from wired_injector.injector import SkipField

                raise SkipField()

        return value
