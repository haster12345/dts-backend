import pytest
from src.app import app

@pytest.fixture
def client():
    """
    Creates a test client fixture for the Flask application.

    This fixture configures the app for testing and yields a test client
    that can be used to send requests to the application during tests.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_tasks(client):
    """
    Tests the GET /tasks endpoint.

    Verifies that:
    1. The endpoint returns a 200 OK status code
    2. The response contains a JSON list of tasks
    """
    response = client.get('/tasks')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_create_task_success(client):
    """
    Tests successful task creation via POST /create-task endpoint.

    Sends a new task JSON payload and verifies:
    1. The endpoint returns a 200 OK status code
    2. The response JSON contains a status code of 204 (No Content)
       indicating successful creation without returned content
    """
    # Sample task data - adjust fields based on your application's requirements
    new_task = {
        "casenum": "12345",
        "description": "Test task",
        "status": "open"
    }
    response = client.post('/create-task', json=new_task)
    assert response.status_code == 200
    assert response.get_json()['status'] == 204

def test_create_task_failure(client, monkeypatch):
    """
    Tests the error handling of the POST /create-task endpoint.

    This test:
    1. Mocks the database create_tasks method to simulate a failure
    2. Verifies the endpoint handles errors gracefully
    3. Checks that appropriate error status and message are returned

    Uses monkeypatch to temporarily replace the real database method with a mock
    that raises an exception.
    """
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
    """
    Tests successful task deletion via DELETE /delete-task/<task_id> endpoint.

    Verifies that:
    1. The endpoint returns a 200 OK status code
    2. The response JSON contains a status code of 204 (No Content)
       indicating successful deletion without returned content

    Note: This test assumes task ID 1 exists in the database. In a real test suite,
    you might want to create a task first or mock the database layer.
    """
    response = client.delete('/delete-task/1')
    assert response.status_code == 200
    assert response.get_json()['status'] == 204

def test_delete_task_failure(client, monkeypatch):
    """
    Tests the error handling of the DELETE /delete-task/<task_id> endpoint.

    This test:
    1. Mocks the database delete_task method to simulate a failure
    2. Verifies the endpoint handles errors gracefully
    3. Checks that appropriate error status and message are returned

    Uses monkeypatch to temporarily replace the real database method with a mock
    that raises an exception.
    """
    def mock_delete_task_failure(*args, **kwargs):
        raise Exception("DB error")

    from src.app import db
    monkeypatch.setattr(db, "delete_task", mock_delete_task_failure)

    response = client.delete('/delete-task/9999')
    assert response.status_code == 200
    assert response.get_json()['status'] == 500
    assert 'error' in response.get_json()