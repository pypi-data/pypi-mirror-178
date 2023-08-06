import datetime

from fastapi.testclient import TestClient
from pydantic import BaseModel

from testdb import override_get_session
from compute_service import ComputeService
from compute_service.api import models


class TestModel(BaseModel):
    title: str
    value: int


service = ComputeService(queue='test')
app = service.create_app(TestModel)

from compute_service.routers.tasks import get_session
app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


def test_post_task():
    response = client.get("/api/v1.0/tasks")
    assert response.status_code == 200

    response = client.post(
        "/api/v1.0/tasks/",
        json={
            "input_params": { 
                "title": "test title",
                "value": 123
            }
        },
    )
    print(response.json())
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["input_params"]["title"] == "test title"
    assert data["input_params"]["value"] == 123
    assert "uuid" in data
    task_id = data["uuid"]

    response = client.get(f"/api/v1.0/tasks/{task_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["input_params"]["title"] == "test title"
    assert data["input_params"]["value"] == 123
    assert data["uuid"] == task_id

    date_started = datetime.datetime.now()
    date_finished = datetime.datetime.now()
    date_format = '%Y-%m-%dT%H:%M:%S.%f'

    response = client.patch(
        f"/api/v1.0/tasks/{task_id}",
        json={
            "status": models.Status.in_progress,
            "started": str(date_started)
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert models.Status(data["status"]) == models.Status.in_progress

    response = client.patch(
        f"/api/v1.0/tasks/{task_id}",
        json={
            "status": models.Status.success,
            "finished": str(date_finished),
            "result": {"ok": "success"}
        },
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["uuid"] == task_id
    assert models.Status(data["status"]) == models.Status.success
    assert datetime.datetime.strptime(data["started"], date_format) == date_started
    assert datetime.datetime.strptime(data["finished"], date_format) == date_finished
    assert data["result"]["ok"] == "success"

    response = client.delete(f"/api/v1.0/tasks/{task_id}")
    assert response.status_code == 204
