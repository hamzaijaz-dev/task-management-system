from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class Todo(Base):
    __tablename__ = "todo_todo"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(DateTime)
    priority = Column(String)
    status = Column(String)
    creator_id = Column(Integer)
    assigned_to_id = Column(Integer, nullable=True)
