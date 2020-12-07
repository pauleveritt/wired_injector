from typing import Optional

from wired import ServiceContainer
from wired_injector.injector import Injector
from wired_injector.operators import Get, Attr, Context

from examples.factories import (
    Customer,
    View,
    FrenchView,
)

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


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
    result: View = injector(target)
    assert result.name == 'View'


def test_one_parameter_field_type(regular_container):
    def target(view: View):
        return view

    injector = Injector(regular_container)
    result: View = injector(target)
    assert result.name == 'View'


def test_one_parameter_annotated(french_container):
    def target(
            french_view: Annotated[
                FrenchView,
                Get(View),
            ]
    ):
        return french_view

    injector = Injector(french_container)
    result: FrenchView = injector(target)
    assert result.name == 'French View'


def test_two_parameters_unannotated(regular_container):
    def target(container: ServiceContainer, view: View):
        return view

    injector = Injector(regular_container)
    result: View = injector(target)
    assert result.name == 'View'


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
    result: Customer = injector(target)
    assert result.name == 'French View'


def test_optional_unannotated(regular_container):
    # TODO: Need Optional[str] = None default value
    def target(container: Optional[ServiceContainer]):
        if container is None:
            return None
        view = container.get(View)
        return view

    injector = Injector(regular_container)
    result: View = injector(target)
    assert result.name == 'View'


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
    result: FrenchView = injector(target)
    assert result.name == 'French View'


def test_props_unannotated_untyped(regular_container):
    def target(container):
        return container

    injector = Injector(regular_container)
    result: int = injector(target, container=88)
    assert 88 == result


def test_props_unannotated_typed(regular_container):
    def target(container: ServiceContainer):
        return container

    injector = Injector(regular_container)
    result: int = injector(target, container=88)
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
    result: View = injector(target)
    assert result == 'View'


def test_default_value_unannotated(regular_container):
    class Foo:
        pass

    f = Foo()

    def target(some_foo: Foo = f) -> Foo:
        return some_foo

    injector = Injector(regular_container)
    result: Foo = injector(target)
    assert result is f


def test_default_value_annotated(regular_container):
    class Foo:
        pass

    def target(
            view_name: Annotated[
                str,
                Get(Foo),
                Attr('name'),
            ] = 'View Name'
    ):
        return view_name

    injector = Injector(regular_container)
    result: str = injector(target)
    assert result == 'View Name'


def test_context_then_attr(regular_container):
    """ Pipeline: Context, Attr """

    def target(
            customer_name: Annotated[
                str,
                Context(),
                Attr('name'),
            ],
    ):
        return customer_name

    injector = Injector(regular_container)
    result: View = injector(target)
    assert result == 'Customer'


def test_system_props_unannotated_untyped(regular_container):
    def target(children):
        return children

    injector = Injector(regular_container)
    system_props = dict(children=77)
    result: int = injector(target, system_props=system_props)
    assert 77 == result
