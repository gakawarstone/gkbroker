from typing import Any
from typing import Dict, Optional, List
import uuid
from collections import deque

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# In-memory stores
task_queue = deque()  # queue of (task_id, function, data)
task_status: Dict[str, str] = {}  # task_id -> "pending" | "processing" | "completed"
task_function: Dict[str, str] = {}  # task_id -> original function
task_data: Dict[str, list[Any]] = {}  # task_id -> original data
task_results: Dict[str, str] = {}  # task_id -> result


# Models
class TaskPayload(BaseModel):
    function: str
    data: list[Any]


class TaskResult(BaseModel):
    task_id: str
    result: str


# Enqueue a new task
@app.post("/enqueue")
async def enqueue_task(payload: TaskPayload):
    task_id = str(uuid.uuid4())
    task_queue.append((task_id, payload.function, payload.data))
    task_status[task_id] = "pending"
    task_function[task_id] = payload.function
    task_data[task_id] = payload.data
    return {"task_id": task_id, "status": "pending"}


# Worker fetches next pending task
@app.get("/get_task")
async def get_task(function: str):
    if not task_queue:
        return {"task_id": None, "function": None, "data": None}

    # Find the first task with the specified function
    for i, (task_id, task_fn, data) in enumerate(task_queue):
        if task_fn == function:
            # Remove the task from the deque
            del task_queue[i]
            task_status[task_id] = "processing"
            return {"task_id": task_id, "function": task_fn, "data": data}
            
    # No task with the specified function was found
    return {"task_id": None, "function": None, "data": None}


# Worker submits result
@app.post("/submit_result")
async def submit_result(result: TaskResult):
    if result.task_id not in task_status:
        return {"error": "Invalid task_id"}
    task_results[result.task_id] = result.result
    task_status[result.task_id] = "completed"
    return {"status": "completed", "task_id": result.task_id}


# Client checks task result
@app.get("/result/{task_id}")
async def get_result(task_id: str):
    status = task_status.get(task_id)
    if not status:
        return {"error": "Task not found"}
    result = task_results.get(task_id)
    return {"task_id": task_id, "status": status, "result": result}