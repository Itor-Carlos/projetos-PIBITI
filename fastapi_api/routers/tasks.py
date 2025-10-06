from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.task_service import TaskService
from schemas import TaskCreate, TaskResponse, TaskUpdate
from typing import List

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    return TaskService(db).list_tasks()

@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return TaskService(db).create_task(task)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    updated = TaskService(db).update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return updated

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = TaskService(db).delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa removida com sucesso"}
