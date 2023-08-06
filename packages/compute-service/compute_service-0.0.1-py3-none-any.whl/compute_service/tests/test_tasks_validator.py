from fastapi.testclient import TestClient
from pydantic import BaseModel

from testdb import override_get_session
from compute_service import ComputeService


class TestModel(BaseModel):
    title: str
    value: int


def validator(input_params):
    if input_params['value'] < 1:
        raise ValueError('Value < 1')


service = ComputeService(queue='test')
app = service.create_app(TestModel, input_validator=validator)

from compute_service.routers.tasks import get_session
app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


def test_task_validator():
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

    response = client.post(
        "/api/v1.0/tasks/",
        json={
            "input_params": { 
                "title": "test title",
                "value": -3
            }
        },
    )
    print(response.json())
    assert response.status_code == 409, response.text
