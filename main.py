from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import engine, SessionLocal
from schemas import TodoRequest
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependencies = Annotated[Session, Depends(get_db)]


@app.get('/', status_code=status.HTTP_200_OK)
def all_todos(db: db_dependencies):
    return db.query(models.Todos).all()


@app.post('/create_todo', status_code=status.HTTP_201_CREATED)
def create_todo(request: TodoRequest, db: db_dependencies):
    task = models.Todos(**request.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
