from app.config import Settings
from app.vision.service import analyze_image
from tests.helpers import fixture_bytes


def test_starter_detection_pipeline_uses_detection_fixture() -> None:
    result = analyze_image(
        image_bytes=fixture_bytes("detection-scene.png"),
        filename="detection-scene.png",
        content_type="image/png",
        pipeline_id="starter-detection",
        settings=Settings(),
    )

    assert result.pipeline.id == "starter-detection"
    assert result.image.width == 320
    assert result.image.height == 240
    assert len(result.detections) >= 2
    assert result.detections[0].label == "primary-object"
    assert result.segmentations == []
    assert any(metric.name == "edge_density" for metric in result.metrics)


def test_document_layout_pipeline_uses_document_fixture() -> None:
    result = analyze_image(
        image_bytes=fixture_bytes("document-layout.png"),
        filename="document-layout.png",
        content_type="image/png",
        pipeline_id="document-layout",
        settings=Settings(),
    )

    assert result.pipeline.id == "document-layout"
    assert len(result.detections) >= 1
    assert any(
        detection.label == "document-candidate"
        for detection in result.detections
    )
    assert any(metric.name == "layout_candidates" for metric in result.metrics)


def test_foreground_segmentation_pipeline_uses_segmentation_fixture() -> None:
    result = analyze_image(
        image_bytes=fixture_bytes("segmentation-scene.png"),
        filename="segmentation-scene.png",
        content_type="image/png",
        pipeline_id="foreground-segmentation",
        settings=Settings(),
    )

    assert result.pipeline.id == "foreground-segmentation"
    assert len(result.segmentations) >= 2
    assert result.segmentations[0].polygon
    assert result.segmentations[0].box.width < result.image.width
    assert any(metric.name == "segmented_regions" for metric in result.metrics)
