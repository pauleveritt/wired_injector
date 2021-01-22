from typing import Optional, NamedTuple

from wired import ServiceContainer
from wired_injector.injector import Injector
from wired_injector.operators import Get, Attr

from examples.factories import (
    View,
    FrenchView,
)

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore  # noqa: F401


# Damn, mypy bug with nested named tuples
# https://github.com/python/mypy/issues/7281
class Target1(NamedTuple):
    def __call__(self) -> int:
        return 99


def test_no_parameters(regular_container):
    injector = Injector(regular_container)
    target: Target1 = injector(Target1)
    result: int = target()
    assert result == 99


class Target2(NamedTuple):
    container: ServiceContainer

    def __call__(self):
        view = self.container.get(View)
        return view


def test_one_parameter_container(regular_container):
    injector = Injector(regular_container)
    target: Target2 = injector(Target2)
    result: View = target()
    assert result.name == 'View'


class Target3(NamedTuple):
    view: View

    def __call__(self) -> View:
        return self.view


def test_one_parameter_field_type(regular_container):
    injector = Injector(regular_container)
    target: Target3 = injector(Target3)
    result: View = target()
    assert result.name == 'View'


class Target4(NamedTuple):
    french_view: Annotated[
        FrenchView,
        Get(View),
    ]

    def __call__(self):
        return self.french_view


def test_one_parameter_annotated(french_container):
    injector = Injector(french_container)
    target: Target4 = injector(Target4)
    result: FrenchView = target()
    assert result.name == 'French View'


class Target5(NamedTuple):
    container: ServiceContainer
    view: View

    def __call__(self) -> View:
        return self.view


def test_two_parameters_unannotated(regular_container):
    injector = Injector(regular_container)
    target: Target5 = injector(Target5)
    result: View = target()
    assert result.name == 'View'


class Target6(NamedTuple):
    container: ServiceContainer
    french_customer: Annotated[
        FrenchView,
        Get(View),
    ]

    def __call__(self):
        return self.french_customer


def test_two_parameters_annotated(french_container):
    injector = Injector(french_container)
    target: Target6 = injector(Target6)
    result: FrenchView = target()
    assert result.name == 'French View'


class Target7(NamedTuple):
    container: Optional[ServiceContainer]

    def __call__(self) -> Optional[View]:
        if self.container is None:
            return None
        view = self.container.get(View)
        return view


def test_optional_unannotated(regular_container):
    injector = Injector(regular_container)
    target: Target7 = injector(Target7)
    result: Optional[View] = target()
    if result is not None:
        assert result.name == 'View'


class Target8(NamedTuple):
    french_customer: Optional[
        Annotated[
            FrenchView,
            Get(View),
        ]
    ]

    def __call__(self):
        return self.french_customer


def test_optional_annotated(french_container):
    injector = Injector(french_container)
    target: Target8 = injector(Target8)
    result: FrenchView = target()
    assert result.name == 'French View'


class Target9(NamedTuple):
    container: ServiceContainer
    flag: int

    def __call__(self):
        return self.flag


def test_props_extra(regular_container):
    # Send an extra prop, not one that overrides an injected prop

    injector = Injector(regular_container)
    target: Target9 = injector(Target9, flag=88)
    result: int = target()
    assert 88 == result


class Target10(NamedTuple):
    container: ServiceContainer

    def __call__(self):
        return self.container


def test_props_override(regular_container):
    # Send a prop that overrides an injected prop

    injector = Injector(regular_container)
    target: Target10 = injector(Target10, container=88)
    result = target()
    assert 88 == result


class Target11(NamedTuple):
    customer_name: Annotated[
        str,
        Get(View),
        Attr('name'),
    ]

    def __call__(self):
        return self.customer_name


def test_get_then_attr(regular_container):
    """ Pipeline: Get, Attr """

    injector = Injector(regular_container)
    target: Target11 = injector(Target11)
    result: str = target()
    assert result == 'View'
