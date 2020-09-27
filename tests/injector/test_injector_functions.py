from typing import Optional, Annotated

from wired import ServiceContainer
from wired_injector.injector import Injector
from wired_injector.operators import Get, Attr

from ..conftest import RegularCustomer, FrenchCustomer, View, RegularView, FrenchView


def test_construction(regular_container):
    injector = Injector(regular_container)
    assert injector


def test_no_parameters(regular_container):
    def target():
        return 99

    injector = Injector(regular_container)
    result: int = injector(target)
    assert result == 99


def test_one_parameter_container(regular_container):
    def target(container: ServiceContainer):
        view = container.get(View)
        return view

    injector = Injector(regular_container)
    result: RegularView = injector(target)
    assert result.name == 'Regular View'


def test_one_parameter_field_type(regular_container):
    def target(view: View):
        return view

    injector = Injector(regular_container)
    result: RegularView = injector(target)
    assert result.name == 'Regular View'


def test_one_parameter_annotated(french_container):
    def target(french_view: Annotated[
        FrenchView,
        Get(View),
    ]):
        return french_view

    injector = Injector(french_container)
    result = injector(target)
    assert result.name == 'French View'


def test_two_parameters_unannotated(regular_container):
    def target(container: ServiceContainer, view: View):
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
    result: RegularCustomer = injector(target)
    assert result.name == 'French View'


def test_optional_unannotated(regular_container):
    # TODO: Need Optional[str] = None default value
    def target(container: Optional[ServiceContainer]):
        view = container.get(View)
        return view

    injector = Injector(regular_container)
    result = injector(target)
    assert result.name == 'Regular View'


def test_optional_annotated(french_container):
    def target(
            french_view: Optional[
                Annotated[
                    FrenchView,
                    Get(View),
                ]
            ],
    ):
        return french_view

    injector = Injector(french_container)
    result = injector(target)
    assert result.name == 'French View'


def test_props_unannotated(regular_container):
    def target(container: ServiceContainer):
        return container

    injector = Injector(regular_container)
    result = injector(target, container=88)
    assert 88 == result


def test_get_then_attr(regular_container):
    """ Pipeline: Get, Attr """

    def target(
            view_name: Annotated[
                str,
                Get(View),
                Attr('name'),
            ],
    ):
        return view_name

    injector = Injector(regular_container)
    result = injector(target)
    assert result == 'Regular View'
