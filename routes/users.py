from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from passlib.context import CryptContext

from database import SessionLocal
from models import User

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str = Field()
    email: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    password: str = Field()
    role: str = Field()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependencies = Annotated[Session, Depends(get_db)]


@router.post('/auth', status_code=status.HTTP_201_CREATED)
def user_registration(db: db_dependencies, new_user: CreateUserRequest):
    new_user_instance = User(
        email=new_user.email,
        username=new_user.username,
        password=bcrypt_context.hash(new_user.password),
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        role="admin",
        is_active=True
    )

    db.add(new_user_instance)
    db.commit()
    return new_user_instance
