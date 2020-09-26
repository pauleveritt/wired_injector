from dataclasses import dataclass
from typing import Optional, Annotated

from wired import ServiceContainer
from wired_injector.injector import Injector
from wired_injector.operators import Get, Attr

from ..conftest import View, FrenchView, RegularView


def test_one_parameter_container(regular_container):
    @dataclass
    class Target:
        container: ServiceContainer

        def __call__(self):
            view = self.container.get(View)
            return view

    injector = Injector(regular_container)
    target = injector(Target)
    result = target()
    assert result.name == 'Regular View'


def test_one_parameter_field_type(regular_container):
    @dataclass
    class Target:
        view: View

        def __call__(self):
            return self.view

    injector = Injector(regular_container)
    target = injector(Target)
    result = target()
    assert result.name == 'Regular View'


def test_one_parameter_annotated(french_container):
    def target(
            french_view: Annotated[
                FrenchView,
                Get(View),
            ]
    ):
        return french_view

    injector = Injector(french_container)
    result = injector(target)
    assert result.name == 'French View'


def test_two_parameters_unannotated(regular_container):
    def target(
            container: ServiceContainer,
            view: View,
    ):
        return view

    injector = Injector(regular_container)
    result: RegularView = injector(target)
    assert result.name == 'Regular View'


def test_two_parameters_annotated(french_container):
    def target(
            container: ServiceContainer,
            french_customer: Annotated[
                FrenchView,
                Get(View),
            ],
    ):
        return french_customer

    injector = Injector(french_container)
    result: FrenchView = injector(target)
    assert result.name == 'French View'


def test_optional_unannotated(regular_container):
    def target(container: Optional[ServiceContainer]):
        view = container.get(View)
        return view

    injector = Injector(regular_container)
    result: RegularView = injector(target)
    assert result.name == 'Regular View'


def test_optional_annotated(french_container):
    def target(
            french_customer: Optional[Annotated[
                FrenchView,
                Get(View),
            ]
            ],
    ):
        return french_customer

    injector = Injector(french_container)
    result = injector(target)
    assert result.name == 'French View'


def test_props_extra(regular_container):
    # Send an extra prop, not one that overrides an injected prop
    def target(container: ServiceContainer, flag: int):
        return flag

    injector = Injector(regular_container)
    result = injector(target, flag=88)
    assert 88 == result


def test_props_override(regular_container):
    # Send a prop that overrides an injected prop
    def target(container: ServiceContainer):
        return container

    injector = Injector(regular_container)
    result = injector(target, container=88)
    assert 88 == result


def test_get_then_attr(regular_container):
    """ Pipeline: Get, Attr """

    def target(
            customer_name: Annotated[
                str,
                Get(View),
                Attr('name'),
            ],
    ):
        return customer_name

    injector = Injector(regular_container)
    result = injector(target)
    assert result == 'Regular View'
