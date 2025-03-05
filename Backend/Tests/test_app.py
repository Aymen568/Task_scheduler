# backend/tests/test_app.py
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the app object
from app import app

import pytest

# Test fixtures
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test cases
def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.json == []

def test_add_task(client):
    response = client.post('/tasks', json={
        'topic': 'Test Topic',
        'title': 'Test Task',
        'description': 'Test Description',
        'timeStart': '2023-10-01T09:00',
        'timeEnd': '2023-10-01T12:00',
        'dependencies': '1'
    })
    assert response.status_code == 201
    assert response.json['topic'] == 'Test Topic'

def test_delete_task(client):
    # Add a task first and verify it has been added successfully
    task_informations = {
        'topic': 'Test Topic',
        'title': 'Test Task',
        'description': 'Test Description',
        'timeStart': '2023-10-01T09:00',
        'timeEnd': '2023-10-01T12:00',
        'dependencies': '1'
    }

    # Add the task
    add_response = client.post('/tasks', json=task_informations)
    assert add_response.status_code == 201  # Verify the task was added successfully

    # Retrieve the task ID from the response
    added_task = add_response.json
    task_id = added_task['id']  # Extract the task ID

    # Verify the task is in the list
    get_response = client.get('/tasks')
    assert get_response.status_code == 200
    tasks = get_response.json
    assert any(task['id'] == task_id for task in tasks)  # Verify the task exists

    # Delete the task
    delete_response = client.delete(f'/tasks/{task_id}')
    assert delete_response.status_code == 204  # Verify the task was deleted successfully

    # Verify the task is no longer in the list
    get_response_after_delete = client.get('/tasks')
    assert get_response_after_delete.status_code == 200
    tasks_after_delete = get_response_after_delete.json
    assert all(task['id'] != task_id for task in tasks_after_delete)  # Verify the task is deleted

    
# Run tests
if __name__ == '__main__':
    pytest.main()

    