from fastapi import HTTPException
from pydantic import EmailStr
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models import User
from datetime import datetime
from domain.user.user_schema import UserCreate, UserUpdate
from domain.common.enums import Telecom, Gender

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email,
                   name=user_create.name,
                   birthdate=user_create.birthdate,
                   gender=user_create.gender,
                   telecom=user_create.telecom,
                   phone_number=user_create.phone_number
                   )
    db.add(db_user)
    db.commit()

def is_username_exists(db: Session, username: str) -> bool:
    return db.query(User).filter(User.username == username).first() is not None

def is_email_exists(db: Session, email: str) -> bool:
    return db.query(User).filter(User.email == email).first() is not None

def is_phone_exists(db: Session, phone_number: str) -> bool:
    return db.query(User).filter(User.phone_number == phone_number).first() is not None

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def verify_user_password(db: Session, user_id: int, password: str) -> bool:
    user = get_user_by_id(db, user_id)
    if user and pwd_context.verify(password, user.password):
        return True
    return False

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()

def update_login_info(db: Session, user: User):
    user.last_login = datetime.utcnow()
    user.login_count = (user.login_count or 0) + 1
    db.commit()

def update_user_info(db: Session, user: User, data: UserUpdate):
    if data.name is not None:
        user.name = data.name
    if data.username is not None:
        if db.query(User).filter(User.username == data.username).first():
            raise HTTPException(status_code=409, detail="이미 존재하는 아이디입니다.")
        user.username = data.username
    if data.email is not None:
        user.email = data.email
    if data.telecom is not None:
        user.telecom = data.telecom
    if data.phone_number is not None:
        user.phone_number = data.phone_number
    db.commit()

def update_password(db: Session, user: User, new_password: str):
    user.password = pwd_context.hash(new_password)
    db.commit()
