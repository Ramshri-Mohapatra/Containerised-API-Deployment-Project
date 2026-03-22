import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import routes

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_tasks():
    routes.tasks.clear()
    yield
    routes.tasks.clear()
#Root endpoint

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "is running" in response.json()["message"]

#Create tasks

def test_get_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

#Create a task

def test_create_task():
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "This is a test",
        "completed": False
    })
    assert response.status_code == 200
    assert response.json()["task"]["title"] == "Test Task"

def test_create_task_missing_title():
    response = client.post("/tasks", json={"description": "No title provided"})
    assert response.status_code == 422

#Get a single task
def test_get_task():
    client.post("/tasks", json={"title": "Get Me"})
    response = client.get("/tasks/0")
    assert response.status_code == 200
    assert response.json()["title"] == "Get Me"

def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

#Delete Task
def test_delete_task():
    client.post("/tasks", json={"title": "Delete Me"})
    response = client.delete("/tasks/0")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"

def test_delete_task_not_found():
    response = client.delete("/tasks/999")
    assert response.status_code == 404