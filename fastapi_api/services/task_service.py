from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def list_tasks(self):
        return self.db.query(Task).all()

    def create_task(self, task_data: TaskCreate):
        task = Task(**task_data.dict())
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task(self, task_id: int, task_data: TaskUpdate):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None
        for field, value in task_data.dict(exclude_unset=True).items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True
