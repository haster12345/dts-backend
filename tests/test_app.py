import pytest
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_create_task_success(client):
    # You should adapt this JSON based on what your db.create_tasks expects
    new_task = {
        "casenum": "12345",
        "description": "Test task",
        "status": "open"
    }
    response = client.post('/create-task', json=new_task)
    assert response.status_code == 200
    assert response.get_json()['status'] == 204

def test_create_task_failure(client, monkeypatch):
    # Simulate a failure inside db.create_tasks
    def mock_create_tasks_failure(*args, **kwargs):
        raise Exception("DB error")

    from src.app import db
    monkeypatch.setattr(db, "create_tasks", mock_create_tasks_failure)

    response = client.post('/create-task', json={})
    assert response.status_code == 200
    assert response.get_json()['status'] == 500
    assert 'error' in response.get_json()

def test_delete_task_success(client):
    # Assuming task with id=1 exists. You may need to mock db for a clean test.
    response = client.delete('/delete-task/1')
    assert response.status_code == 200
    assert response.get_json()['status'] == 204

def test_delete_task_failure(client, monkeypatch):
    def mock_delete_task_failure(*args, **kwargs):
        raise Exception("DB error")

    from src.app import db
    monkeypatch.setattr(db, "delete_task", mock_delete_task_failure)

    response = client.delete('/delete-task/9999')
    assert response.status_code == 200
    assert response.get_json()['status'] == 500
    assert 'error' in response.get_json()

