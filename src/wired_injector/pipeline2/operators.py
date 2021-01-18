"""
Implementations of major operators such as ``Get``.
"""
from dataclasses import dataclass
from inspect import isclass, signature
from typing import Any, Optional

from . import Result, Pipeline
from .results import Error, Found, NotFound


@dataclass(frozen=True)
class Get:
    """ Which service in the container to get """

    lookup_key: Any
    attr: Optional[str] = None

    def __call__(
        self,
        previous: Optional[Result],
        pipeline: Pipeline,
    ) -> Result:

        # Can't lookup a string, ever, so bail on this with an error.
        if isinstance(self.lookup_key, str):
            lk = self.lookup_key
            msg = f"Cannot use a string '{lk}' as container lookup value"
            return Error(msg=msg, value=Get)

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
        previous: Optional[Result],
        pipeline: Pipeline,
    ) -> Result:
        if previous is None:
            # This operator is being used first in the pipeline
            # which then means we are trying to do getattr on
            # None. Raise a specific error.
            msg = "Cannot use 'Attr' operator first in the pipeline"
            return NotFound(msg=msg, value=Attr)

        # Get the value out of the Result passed in as previous
        previous_value: Any = previous.value
        value = getattr(previous_value, self.name)
        return Found(value=value)


@dataclass(frozen=True)
class Context:
    """ Get the current container's context object. """

    attr: Optional[str] = None

    def __call__(
        self,
        previous: Optional[Result],
        pipeline: Pipeline,
    ) -> Result:

        # If the container.context is None, then getting an
        # attr off of it is pointless. Bail out with NotFound
        # and let downstream try to get a field default.
        value = pipeline.container.context
        if value is None:
            msg = f"Container context is None"
            return Error(msg=msg, value=Context)

        if self.attr is not None:
            # Pluck the attribute's value and return that instead
            # of the container.context.
            value = getattr(value, self.attr)

        return Found(value=value)


@dataclass(frozen=True)
class Field:
    """ Get default value field in dataclass/namedtuple being constructed """

    __slots__ = ('name',)
    name: str

    def __call__(
        self,
        previous: Optional[Result],
        pipeline: Pipeline,
    ) -> Result:

        target = pipeline.target
        # TODO Eventually we could avoid the cost of doing this signature
        #   by either storing on Pipeline or even having a registry
        #   factory (across containers/requests) that fetched the signature
        #   for a callable.
        sig = signature(target)
        try:
            param = sig.parameters[self.name]
        except KeyError:
            msg = f'No field "{self.name}" on target'
            return Error(msg=msg, value=Field)
        return Found(value=param.default)
