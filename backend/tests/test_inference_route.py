from fastapi.testclient import TestClient

from app.main import app
from tests.helpers import fixture_bytes

client = TestClient(app)


def test_analyze_route_accepts_fixture_upload() -> None:
    response = client.post(
        "/api/v1/analyze",
        data={"pipeline_id": "starter-detection"},
        files={
            "file": (
                "detection-scene.png",
                fixture_bytes("detection-scene.png"),
                "image/png",
            )
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["pipeline"]["id"] == "starter-detection"
    assert payload["image"]["filename"] == "detection-scene.png"
    assert len(payload["detections"]) >= 2


def test_analyze_route_rejects_non_image_upload() -> None:
    response = client.post(
        "/api/v1/analyze",
        data={"pipeline_id": "starter-detection"},
        files={"file": ("notes.txt", b"not-an-image", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only image uploads are supported."
