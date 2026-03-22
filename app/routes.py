import logging
from fastapi import APIRouter, HTTPException
from app.models import Task

logger = logging.getLogger(__name__)

router = APIRouter()

#In-memory storage

tasks = []

@router.get("/tasks")
def get_tasks():
    logger.info(f"Fetching all tasks - {len(tasks)} tasks found")
    return tasks

@router.post("/tasks")
def create_tasks(task: Task):
    tasks.append(task)
    logger.info(f"Task created: {task.title}")
    return{"message": "Task created", "task": task}

@router.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id >= len(tasks) or task_id < 0:
        logger.warning(f"Task {task_id} not found")
        raise HTTPException(status_code=404, detail ="Task not found")
    logger.info(f"Fetching task {task_id}")
    return tasks[task_id]

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id >= len(tasks) or task_id < 0:
        logger.warning(f"Attempted to delete non-existent task {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    deleted = tasks.pop(task_id)
    logger.info(f"Task deleted: {deleted.title}")
    return {"message": "Task deleted"}