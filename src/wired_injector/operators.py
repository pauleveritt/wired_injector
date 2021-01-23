# from dataclasses import dataclass
# from inspect import isclass, signature
# from typing import Type, Any, Optional
#
# # TODO Operator should be a Protocol but the typechecker then says a usage
# #   in an annotation should be a generic.
# from wired_injector.pipeline import Pipeline
#
#
# class Operator:  # pragma: no cover
#     """ Part of a pipeline for field construction """
#
#     def __call__(
#         self,
#         previous: Any,
#         pipeline: Pipeline,
#     ) -> Any:
#         ...
#
#
# @dataclass(frozen=True)
# class Get(Operator):
#     """ Which service in the container to get """
#
#     # Can't do slots because of default value
#     lookup_type: Type
#     attr: Optional[str] = None
#
#     def __call__(
#         self,
#         previous: Optional[Type],
#         pipeline: Pipeline,
#     ):
#         try:
#             container = pipeline.container
#             service = container.get(self.lookup_type)
#             if isclass(service):
#                 # This "service" is actually injectable, instead of
#                 # a plain factory. At the moment, we just have a class.
#                 # Use this injector instance to turn it into an instance.
#                 from wired_injector import Injector
#
#                 injector = container.get(Injector)
#                 service = injector(service)
#             if self.attr is None:
#                 return service
#             else:
#                 return getattr(service, self.attr)
#         except LookupError:
#             # We don't want to just crash with a LookupError, as the
#             # field might have a default. Thus, bail out of processing
#             # the pipeline.
#             from wired_injector.injector import SkipField
#
#             raise SkipField()
#
#
# @dataclass(frozen=True)
# class Attr(Operator):
#     """ Pluck an attribute off the object coming in """
#
#     __slots__ = ('name',)
#     name: str
#
#     def __call__(
#         self,
#         previous: Any,
#         pipeline: Pipeline,
#     ):
#         raise NotImplementedError()
#         return getattr(previous, self.name)
#
#
# @dataclass(frozen=True)
# class Context(Operator):
#     """ Get the current container's context object. """
#
#     attr: Optional[str] = None
#
#     def __call__(
#         self,
#         previous: Any,
#         pipeline: Pipeline,
#     ):
#         context = pipeline.container.context
#         if self.attr is not None:
#             if context is not None:
#                 return getattr(context, self.attr)
#             else:
#                 # Asking for an attr when the container.context
#                 # is None is an error, perhaps this field has a
#                 # default.
#                 from wired_injector.injector import SkipField
#
#                 raise SkipField()
#
#         return context
#
#
# @dataclass(frozen=True)
# class Field(Operator):
#     """ Get default value field in dataclass/namedtuple being constructed """
#
#     __slots__ = ('name',)
#     name: str
#
#     def __call__(
#         self,
#         previous: Any,
#         pipeline: Pipeline,
#     ):
#         target = pipeline.target
#         sig = signature(target)
#         try:
#             param = sig.parameters[self.name]
#         except KeyError:
#             msg = f'No field "{self.name}" on target "{target.__name__}"'
#             raise KeyError(msg)
#         return param.default
