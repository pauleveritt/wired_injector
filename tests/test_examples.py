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
    ],
)
def test_examples(target):
    expected, actual = target.test()
    assert expected == actual
