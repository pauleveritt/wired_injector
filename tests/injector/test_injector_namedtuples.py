from typing import Optional, NamedTuple

from wired import ServiceContainer
from wired_injector.injector import Injector
from wired_injector.operators import Get, Attr

from ..conftest import View, FrenchView, RegularView

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_no_parameters(regular_container):
    class Target(NamedTuple):

        def __call__(self) -> int:
            return 99

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result: int = target()
    assert result == 99


def test_one_parameter_container(regular_container):
    class Target(NamedTuple):
        container: ServiceContainer

        def __call__(self):
            view = self.container.get(View)
            return view

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result: RegularView = target()
    assert result.name == 'Regular View'


def test_one_parameter_field_type(regular_container):
    class Target(NamedTuple):
        view: View

        def __call__(self) -> View:
            return self.view

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result: View = target()
    assert result.name == 'Regular View'


def test_one_parameter_annotated(french_container):
    class Target(NamedTuple):
        french_view: Annotated[
            FrenchView,
            Get(View),
        ]

        def __call__(self):
            return self.french_view

    injector = Injector(french_container)
    target: Target = injector(Target)
    result: FrenchView = target()
    assert result.name == 'French View'


def test_two_parameters_unannotated(regular_container):
    class Target(NamedTuple):
        container: ServiceContainer
        view: View

        def __call__(self) -> View:
            return self.view

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result: View = target()
    assert result.name == 'Regular View'


def test_two_parameters_annotated(french_container):
    class Target(NamedTuple):
        container: ServiceContainer
        french_customer: Annotated[
            FrenchView,
            Get(View),
        ]

        def __call__(self):
            return self.french_customer

    injector = Injector(french_container)
    target: Target = injector(Target)
    result: FrenchView = target()
    assert result.name == 'French View'


def test_optional_unannotated(regular_container):
    class Target(NamedTuple):
        container: Optional[ServiceContainer]

        def __call__(self) -> Optional[View]:
            if self.container is None:
                return None
            view = self.container.get(View)
            return view

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result: Optional[View] = target()
    if result is not None:
        assert result.name == 'Regular View'


def test_optional_annotated(french_container):
    class Target(NamedTuple):
        french_customer: Optional[Annotated[
            FrenchView,
            Get(View),
        ]]

        def __call__(self):
            return self.french_customer

    injector = Injector(french_container)
    target: Target = injector(Target)
    result: FrenchView = target()
    assert result.name == 'French View'


def test_props_extra(regular_container):
    # Send an extra prop, not one that overrides an injected prop

    class Target(NamedTuple):
        container: ServiceContainer
        flag: int

        def __call__(self):
            return self.flag

    injector = Injector(regular_container)
    target: Target = injector(Target, flag=88)
    result: int = target()
    assert 88 == result


def test_props_override(regular_container):
    # Send a prop that overrides an injected prop

    class Target(NamedTuple):
        container: ServiceContainer

        def __call__(self):
            return self.container

    injector = Injector(regular_container)
    target: Target = injector(Target, container=88)
    result = target()
    assert 88 == result


def test_get_then_attr(regular_container):
    """ Pipeline: Get, Attr """

    class Target(NamedTuple):
        customer_name: Annotated[
            str,
            Get(View),
            Attr('name'),
        ]

        def __call__(self):
            return self.customer_name

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result: str = target()
    assert result == 'Regular View'
