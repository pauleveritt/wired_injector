# """
# Injectable view which doesn't need the ``__wired_factory__`` protocol.
# """
# from dataclasses import dataclass
#
# from wired_injector import injectable, Injector
#
#
#
# @injectable()
# @dataclass
# class View:
#     name: str = 'View'
#
#
# @injectable()
# @dataclass
# class OverriddenView:
#     name: str = 'Overridden View'
#
#
# # The app
# registry = example_registry(__package__)
#
# # Per "request"
# container = registry.create_container()
# injector = Injector(container)
# container.register_singleton(injector)
#
# view: OverriddenView = container.get(View)
# result = view.name
# expected = 'Overridden View'
# expected = 'View'
#
#
# def test():
#     return expected, result
