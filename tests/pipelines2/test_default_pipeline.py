from wired_injector.pipeline2 import Pipeline, Container


def test_construction(
    dummy_container: Container,
    dummy_pipeline: Pipeline,
) -> None:
    # Ensure it meets the protocol
    meets_protocol: Pipeline = dummy_pipeline
    assert meets_protocol

    assert dummy_container == dummy_pipeline.container
