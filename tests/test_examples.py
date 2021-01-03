import pytest

from examples.injectables import (
    hello_injectables,
)
# from examples.index import (
#     # pipelines,
# )
from examples.props import props_injection
from examples.registry import (
    regular_registry,
    injector_registry,
)
from examples.usage import (
    simple_factory,
    wired_factory,
    scanner,
    simple_injectable,
    settings_manual,
    injected_settings,
    named_tuples,
    functions,
    replace,
    annotations,
    annotated_namedtuples,
    annotated_functions,
    props,
    custom_prop_value,
    pipelines,
    context,
    context_override,
)


@pytest.mark.parametrize(
    'target',
    [
        regular_registry,
        injector_registry,
        props_injection,
        simple_factory,
        wired_factory,
        scanner,
        simple_injectable,
        settings_manual,
        injected_settings,
        named_tuples,
        functions,
        replace,
        annotations,
        annotated_namedtuples,
        annotated_functions,
        props,
        custom_prop_value,
        pipelines,
        context,
        context_override,
    ],
)
def test_examples(target):
    expected, actual = target.test()
    assert expected == actual


@pytest.mark.parametrize(
    'target',
    [
        hello_injectables,
    ],
)
def test_examples_injectables(target):
    expected, actual = target.test()
    assert expected == actual
