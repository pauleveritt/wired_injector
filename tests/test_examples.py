import pytest

from examples.index import (
    simple_factory,
    injectable_view,
    settings_view,
    injector_settings,
    annotated,
    operators,
)


@pytest.mark.parametrize(
    'target',
    [
        simple_factory,
        injectable_view,
        settings_view,
        injector_settings,
        annotated,
        operators,
    ],
)
def test_examples(target):
    expected, actual = target.test()
    assert expected == actual
