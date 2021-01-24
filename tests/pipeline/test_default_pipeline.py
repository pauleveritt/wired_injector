from dataclasses import dataclass

import pytest
from wired_injector.pipeline import Pipeline, Container
from wired_injector.pipeline.default_pipeline import DefaultPipeline
from wired_injector.pipeline.operators import Get

from .conftest import (
    DummyTarget,
    DummyTargetNamedTuple,
    dummy_target_function,
)

try:
    from typing import Annotated
except ImportError:  # pragma: no cover
    from typing_extensions import Annotated  # type: ignore # noqa: F401


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


def test_apply_pipeline_one(
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


def test_apply_pipeline_error(
    dummy_container: Container,
) -> None:
    @dataclass
    class DummyErrorTarget:
        title: Annotated[str, Get('XXX')]

    pipeline = DefaultPipeline(
        container=dummy_container,
        props=dict(age=99),
        system_props={},
        target=DummyErrorTarget,
    )
    with pytest.raises(ValueError) as exc:
        pipeline()
    msg = 'DummyErrorTarget|title|AnnotationPipeline|Get'
    assert msg in exc.value.args[0]
