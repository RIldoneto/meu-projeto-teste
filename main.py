# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Banco de dados em memória para simplificar
db = {}
id_counter = 1

class Task(BaseModel):
    title: str
    description: str

class TaskResponse(Task):
    id: int

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: Task):
    global id_counter
    new_task = TaskResponse(id=id_counter, **task.dict())
    db[id_counter] = new_task
    id_counter += 1
    return new_task

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db[task_id]

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: Task):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db[task_id] = TaskResponse(id=task_id, **updated_task.dict())
    return db[task_id]

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    del db[task_id]
    return
