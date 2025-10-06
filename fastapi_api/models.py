from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500))
    completed = Column(Boolean, default=False)
    due_date = Column(Date, nullable=True)
