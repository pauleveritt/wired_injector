import pytest

from examples.index import (
    simple_factory,
    injectable_view,
    settings_view,
    injector_settings,
    annotated,
    annotated_namedtuple,
    annotated_functions,
    operators,
    pipelines,
)

from examples.registry import (
    regular_registry,
    injector_registry,
)

from examples.props import props_injection


@pytest.mark.parametrize(
    'target',
    [
        simple_factory,
        injectable_view,
        settings_view,
        injector_settings,
        annotated,
        annotated_namedtuple,
        annotated_functions,
        operators,
        pipelines,
        # regular_registry,
        # injector_registry,
        props_injection,
    ],
)
def test_examples(target):
    expected, actual = target.test()
    assert expected == actual
