from fastapi import APIRouter, HTTPException
from app.models import Task

router = APIRouter()

#In-memory storage

tasks = []

@router.get("/tasks")
def get_tasks():
    return tasks

@router.post("/tasks")
def create_tasks(task: Task):
    tasks.append(task)
    return{"message": "Task created", "task": task}

@router.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id >= len(tasks) or task_id < 0:
        raise HTTPException(status_code=404, detail ="Task mot found")
    return tasks[task_id]

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id >= len(tasks) or task_id < 0:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.pop(task_id)
    return {"message": "Task deleted"}