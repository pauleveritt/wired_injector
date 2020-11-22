from dataclasses import dataclass
from typing import Optional, Annotated, Union

from wired import ServiceContainer, ServiceRegistry
from wired_injector.decorators import register_injectable
from wired_injector.injector import Injector
from wired_injector.operators import Get, Attr, Context

from ..conftest import View, FrenchView, RegularView


def test_no_parameters(regular_container):
    @dataclass
    class Target:

        def __call__(self) -> int:
            return 99

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result: int = target()
    assert result == 99


def test_one_parameter_container(regular_container):
    @dataclass
    class Target:
        container: ServiceContainer

        def __call__(self):
            view = self.container.get(View)
            return view

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result: RegularView = target()
    assert result.name == 'Regular View'


def test_one_parameter_field_type(regular_container):
    @dataclass
    class Target:
        view: View

        def __call__(self):
            return self.view

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result: View = target()
    assert result.name == 'Regular View'


def test_one_parameter_annotated(french_container):
    @dataclass
    class Target:
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
    @dataclass
    class Target:
        container: ServiceContainer
        view: View

        def __call__(self):
            return self.view

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result: View = target()
    assert result.name == 'Regular View'


def test_two_parameters_annotated(french_container):
    @dataclass
    class Target:
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
    @dataclass
    class Target:
        container: Optional[ServiceContainer] = None

        def __call__(self) -> Optional[View]:
            if self.container is None:
                return None
            else:
                view = self.container.get(View)
                return view

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result = target()
    if result is not None:
        assert result.name == 'Regular View'


def test_optional_annotated(french_container):
    @dataclass
    class Target:
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
    @dataclass
    class Target:
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

    @dataclass
    class Target:
        container: ServiceContainer

        def __call__(self):
            return self.container

    injector = Injector(regular_container)
    target: Target = injector(Target, container=88)
    result = target()
    assert 88 == result


def test_get_then_attr(regular_container):
    """ Pipeline: Get, Attr """

    @dataclass
    class Target:
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


def test_get_then_attr_double_injected(regular_container):
    """ An injected attribute is itself injected """

    @dataclass
    class URL:
        name: str = 'Some URL'

        @property
        def caps_name(self):
            return self.name.upper()

    @dataclass
    class Target:
        customer_name: Annotated[
            str,
            Get(URL),
            Attr('caps_name'),
        ]

    registry = ServiceRegistry()
    register_injectable(registry, URL)
    register_injectable(registry, Target)
    this_container = registry.create_container()
    injector = Injector(this_container)
    this_container.register_singleton(injector, Injector)
    target: Target = injector(Target)
    assert 'SOME URL' == target.customer_name


def test_default_value_unannotated(regular_container):
    class Foo:
        pass

    @dataclass
    class Target:
        view_name: Foo = 'View Name'

        def __call__(self) -> Union[Foo, str]:
            return self.view_name

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result: str = target()
    assert result == 'View Name'


def test_default_value_annotated(regular_container):
    class Foo:
        pass

    @dataclass
    class Target:
        view_name: Annotated[
            str,
            Get(Foo),
            Attr('name'),
        ] = 'View Name'

        def __call__(self):
            return self.view_name

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result = target()
    assert result == 'View Name'


def test_context_then_attr(regular_container):
    """ Pipeline: Context, Attr """

    @dataclass
    class Target:
        customer_name: Annotated[
            str,
            Context(),
            Attr('name'),
        ]

        def __call__(self):
            return self.customer_name

    injector = Injector(regular_container)
    target: Target = injector(Target)
    result = target()
    assert result == 'Some Customer'
