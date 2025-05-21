from passlib.context import CryptContext
from sqlalchemy.orm import Session

from domain.user import user_schema
from domain.user.user_schema import UserCreate
from models import User
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    db_user = User(name=user_create.name,
                   username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email)
    db.add(db_user)
    db.commit()

def is_username_exists(db: Session, username: str) -> bool:
    return db.query(User).filter(User.username == username).first() is not None

def is_email_exists(db: Session, email: str) -> bool:
    return db.query(User).filter(User.email == email).first() is not None

def is_phone_exists(db: Session, phone_number: str) -> bool:
    return db.query(User).filter(User.phone_number == phone_number).first() is not None

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def verify_user_password(db: Session, username: str, password: str) -> bool:
    user = db.query(User).filter(User.username == username).first()
    if user and pwd_context.verify(password, user.password):
        return True
    return False

def delete_user(db: Session, username: str):
    user = get_user(db, username)
    if user:
        db.delete(user)
        db.commit()

def update_login_info(db: Session, user: User):
    user.last_login = datetime.utcnow()
    user.login_count = (user.login_count or 0) + 1
    db.commit()

def update_user_info(db: Session, user: User,
                     update_data: user_schema.UserUpdate):
    user.name = update_data.name
    user.email = update_data.email
    user.phone_number = update_data.phone_number
    user.birthdate = update_data.birthdate
    user.gender = update_data.gender
    user.telecom = update_data.telecom
    db.commit()

