from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Mi API de tareas",
    description="Una API simple para gestion de tareas - semana 1",
    version="1.0.0"
)

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    completed: bool = False
    created_at: Optional[str] = None

tasks_db: List[Task] = []
next_id = 1

@app.get("/")
def read_root():
    """ Endpoint de bienvenida"""
    return {
        "message": "¡Bienvenido a mi primera API con FastAPI",
        "version": "1.0.0",
        "endpoints": {
            "crear tarea": "POST/tasks",
            "listar tareas": "GET/tasks",
            "obtener tarea": "GET/tasks/{task_id}",
            "completar tarea": "PUT/task/{task_id}/complete"
        }
    }

@app.post("/tasks", response_model=Task)
def create_task(task: Task ):
    """ Crear una nueva tarea """
    global next_id

    task.id = next_id
    task.created_at = datetime.now().isoformat()
    next_id += 1

    tasks_db.append(task)

    return task

@app.get("/tasks", response_model=List[Task])
def get_tasks(completed: Optional[bool] = None):
    """ Listar todas las tareas, opcionalmente filtradas por estado"""
    if completed is None:
        return tasks_db
    
    return [ task for task in tasks_db if task.completed == completed]

@app.get("tasks/{id_task}", response_model=Task)
def get_task(task_id: int):
    """ Obtener una tarea especifica por ID"""
    for task in tasks_db:
        if task.id == task_id:
            return task
    
    raise HTTPException (status_code=404, detail="Tarea no encontrada")


@app.put("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    """ Marcar una tarea como completada """
    for task in tasks_db:
        if task.id == task_id:
            task.completed == True
            return task
        
    raise HTTPException (status_code=404, detail="Tarea no encontrada")
