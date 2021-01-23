from dataclasses import dataclass, field
from typing import Optional

import pytest
from wired import ServiceContainer
from wired_injector.pipeline2.operators import (
    Attr,
    Context,
    Get,
)

from examples.factories import (
    View,
    FrenchView,
)

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore  # noqa: F401


def test_no_parameters(regular_injector):
    @dataclass
    class Target:
        def __call__(self) -> int:
            return 99

    target: Target = regular_injector(Target)
    result: int = target()
    assert result == 99


def test_one_parameter_container(regular_injector):
    @dataclass
    class Target:
        container: ServiceContainer

        def __call__(self):
            view = self.container.get(View)
            return view

    target: Target = regular_injector(Target)
    result: View = target()
    assert result.name == 'View'


def test_one_parameter_field_type(regular_injector):
    @dataclass
    class Target:
        view: View

        def __call__(self):
            return self.view

    target: Target = regular_injector(Target)
    result: View = target()
    assert result.name == 'View'


def test_one_parameter_annotated(french_injector):
    @dataclass
    class Target:
        french_view: Annotated[
            FrenchView,
            Get(View),
        ]

        def __call__(self):
            return self.french_view

    target: Target = french_injector(Target)
    result: FrenchView = target()
    assert result.name == 'French View'


def test_two_parameters_unannotated(regular_injector):
    @dataclass
    class Target:
        container: ServiceContainer
        view: View

        def __call__(self):
            return self.view

    target: Target = regular_injector(Target)
    result: View = target()
    assert result.name == 'View'


def test_two_parameters_annotated(french_injector):
    @dataclass
    class Target:
        container: ServiceContainer
        french_customer: Annotated[
            FrenchView,
            Get(View),
        ]

        def __call__(self):
            return self.french_customer

    target: Target = french_injector(Target)
    result: FrenchView = target()
    assert result.name == 'French View'


def test_optional_unannotated(regular_injector):
    @dataclass
    class Target:
        container: Optional[ServiceContainer] = None

        def __call__(self) -> Optional[View]:
            if self.container is None:
                return None
            else:
                view = self.container.get(View)
                return view

    target: Target = regular_injector(Target)
    result = target()
    if result is not None:
        assert result.name == 'View'


def test_optional_annotated(french_injector):
    @dataclass
    class Target:
        french_customer: Optional[
            Annotated[
                FrenchView,
                Get(View),
            ]
        ]

        def __call__(self):
            return self.french_customer

    target: Target = french_injector(Target)
    result: FrenchView = target()
    assert result.name == 'French View'


def test_props_extra(regular_injector):
    # Send an extra prop, not one that overrides an injected prop
    @dataclass
    class Target:
        container: ServiceContainer
        flag: int

        def __call__(self):
            return self.flag

    target: Target = regular_injector(Target, flag=88)
    result: int = target()
    assert 88 == result


def test_props_override(regular_injector):
    # Send a prop that overrides an injected prop

    @dataclass
    class Target:
        container: ServiceContainer

        def __call__(self):
            return self.container

    target: Target = regular_injector(Target, container=88)
    result = target()
    assert 88 == result


def test_get_then_attr(regular_injector):
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

    target: Target = regular_injector(Target)
    result: str = target()
    assert result == 'View'


def test_get_then_attr_double_injected(regular_injector):
    """ An injected attribute is itself injected """

    @dataclass
    class Target:
        customer_name: Annotated[
            str,
            Get(View),
            Attr('caps_name'),
        ]

    target: Target = regular_injector(Target)
    assert 'VIEW' == target.customer_name


def test_default_value_unannotated(regular_injector):
    class Foo:
        pass

    f = Foo()

    @dataclass
    class Target:
        view: Foo = f

        def __call__(self) -> Foo:
            return self.view

    target: Target = regular_injector(Target)
    result: Foo = target()
    assert result == f


def test_default_value_annotated(regular_injector):
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

    target: Target = regular_injector(Target)
    result = target()
    assert result == 'View Name'


def test_context_then_attr(regular_injector):
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

    target: Target = regular_injector(Target)
    result = target()
    assert result == 'Customer'


def test_init_false(regular_injector):
    # field(init=False) means no injection
    @dataclass
    class Target:
        title: str = field(init=False)

        def __post_init__(self):
            self.title = 'POST INIT'

    target: Target = regular_injector(Target)
    result: Target = target
    assert 'POST INIT' == result.title


def test_result_notfound(regular_injector):
    # The rules ran and finished with NotFound. Should
    # get a nice LookupError exception message.
    class Foo:
        pass

    @dataclass
    class Target:
        view: Foo

        def __call__(self) -> Foo:
            return self.view

    with pytest.raises(LookupError) as exc:
        regular_injector(Target)
    msg = "Target|view|IsSimpleType: No service 'Foo' found in container"
    assert exc.value.args[0] == msg

