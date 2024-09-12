from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from schemas import TodoRequest
from models import Todos

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependencies = Annotated[Session, Depends(get_db)]


@router.get('/', status_code=status.HTTP_200_OK)
def all_todos(db: db_dependencies):
    return db.query(Todos).all()


@router.post('/create_todo', status_code=status.HTTP_201_CREATED)
def create_todo(request: TodoRequest, db: db_dependencies):
    task = Todos(**request.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put('/update_todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_dependencies, request: TodoRequest, todo_id: int):
    task = db.query(Todos).get(todo_id)

    if task is None:
        raise HTTPException(
            detail=f"Todo with id {todo_id} does not exists.",
            status_code=status.HTTP_404_NOT_FOUND
        )

    for key, value in request.model_dump().items():
        setattr(task, key, value) if value else None

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.delete('/delete_todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db:db_dependencies, todo_id: int):
    task = db.query(Todos).get(todo_id)

    if task is None:
        raise HTTPException(
            detail=f"Todo with id {todo_id} does not exists",
            status_code=status.HTTP_404_NOT_FOUND
        )

    db.delete(task)
    db.commit()
    return task
