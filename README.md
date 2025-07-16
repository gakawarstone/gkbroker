# gkbroker

A simple, in-memory task broker built with FastAPI. This project provides a basic framework for creating, distributing, and monitoring tasks.

## Features

*   **Task Queue:** A simple in-memory queue for managing tasks.
*   **FastAPI Integration:** Built on the modern, fast (high-performance) web framework for building APIs with Python.
*   **Asynchronous by Design:** Leverages Python's `async` and `await` for non-blocking I/O.
*   **Simple API:** Easy-to-use endpoints for enqueuing tasks, fetching tasks for processing, submitting results, and checking task status.

## API Endpoints

### Enqueue a Task

*   **POST** `/enqueue`
*   **Payload:**
    ```json
    {
        "function": "function_name",
        "data": ["any", "data"]
    }
    ```
*   **Response:**
    ```json
    {
        "task_id": "some-uuid",
        "status": "pending"
    }
    ```

### Get a Task

*   **GET** `/get_task`
*   **Response (Task available):**
    ```json
    {
        "task_id": "some-uuid",
        "function": "function_name",
        "data": ["any", "data"]
    }
    ```
*   **Response (No task available):**
    ```json
    {
        "task_id": null,
        "function": null,
        "data": null
    }
    ```

### Submit a Result

*   **POST** `/submit_result`
*   **Payload:**
    ```json
    {
        "task_id": "some-uuid",
        "result": "task result"
    }
    ```
*   **Response:**
    ```json
    {
        "status": "completed",
        "task_id": "some-uuid"
    }
    ```

### Check Task Result

*   **GET** `/result/{task_id}`
*   **Response:**
    ```json
    {
        "task_id": "some-uuid",
        "status": "pending" | "processing" | "completed",
        "result": "task result" | null
    }
    ```

## How to Run

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

## How to Use

1.  **Enqueue a task:**
    ```bash
    curl -X POST http://127.0.0.1:8000/enqueue -H "Content-Type: application/json" -d '''{"function": "my_function", "data": [1, 2, 3]}'''
    ```
2.  **Get a task (by a worker):**
    ```bash
    curl http://127.0.0.1:8000/get_task
    ```
3.  **Submit a result (by a worker):**
    ```bash
    curl -X POST http://127.0.0.1:8000/submit_result -H "Content-Type: application/json" -d '''{"task_id": "your-task-id", "result": "some result"}'''
    ```
4.  **Check the result:**
    ```bash
    curl http://127.0.0.1:8000/result/your-task-id
    ```
