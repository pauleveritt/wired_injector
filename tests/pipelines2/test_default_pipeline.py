from wired_injector.pipeline2 import Pipeline, Container
from wired_injector.pipeline2.default_pipeline import DefaultPipeline

from .conftest import (
    DummyTarget,
    DummyTargetNamedTuple,
    dummy_target_function,
)


def test_construction_dataclass_target(
    dummy_container: Container,
) -> None:
    # Ensure it meets the protocol
    meets_protocol: Pipeline = DefaultPipeline(
        container=dummy_container,
        props={},
        system_props={},
        target=DummyTarget,
    )
    assert meets_protocol

    assert dummy_container == meets_protocol.container
    assert 'age' == meets_protocol.field_infos[0].field_name
    assert 'title' == meets_protocol.field_infos[1].field_name


def test_construction_namedtuple_target(
    dummy_container: Container,
) -> None:
    # Ensure it meets the protocol
    meets_protocol: Pipeline = DefaultPipeline(
        container=dummy_container,
        props={},
        system_props={},
        target=DummyTargetNamedTuple,
    )
    assert meets_protocol

    assert dummy_container == meets_protocol.container
    assert 'age' == meets_protocol.field_infos[0].field_name
    assert 'title' == meets_protocol.field_infos[1].field_name


def test_construction_function_target(
    dummy_container: Container,
) -> None:
    # Ensure it meets the protocol
    meets_protocol: Pipeline = DefaultPipeline(
        container=dummy_container,
        props={},
        system_props={},
        target=dummy_target_function,
    )
    assert meets_protocol

    assert dummy_container == meets_protocol.container
    assert 'age' == meets_protocol.field_infos[0].field_name
    assert 'title' == meets_protocol.field_infos[1].field_name


def test_apply_pipeline(
    dummy_container: Container,
) -> None:
    pipeline = DefaultPipeline(
        container=dummy_container,
        props=dict(age=99),
        system_props={},
        target=DummyTarget,
    )
    dummy_target: DummyTarget = pipeline()
    assert 99 == dummy_target.age
