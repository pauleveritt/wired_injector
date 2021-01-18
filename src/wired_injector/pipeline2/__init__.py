"""
Process fields in a target to produce argument values.

Targets have a list of arguments. Dataclasses/NamedTuples have fields,
functions have arguments, etc. The injector wants to use a little
DSL that goes through each field and gets the value, handling
problems along the way.

Pipeline
========

All the work to collect a dictionary of values to apply for construction.

FieldPipeline
=============

All the work to get the value for one field.

Rules
=====

An ordered list of simple policies to work through in trying to get
a value.

Operator
========

A sequence of input/outputs to work through in trying to get a value.

While these are each intended to be isolated, pure, atomic, etc., in
some cases you want to rely on something elsewhere. For example, the
passed-in prop to refer to a logo might be used to resolve into a full
relative link.
"""

__all__ = [
    'Container',
    'FieldInfo',
    'Operator',
    'Result',
    'Rule',
    'Pipeline',
]

from .protocols import (
    Container,
    FieldInfo,
    Operator,
    Result,
    Rule,
    Pipeline,
)
