from datetime import timedelta, datetime, UTC
import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from dotenv import load_dotenv

from models import User as ModelUser
from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context
from domain.user.user_schema import PasswordVerify
from domain.user.user_schema import UserUpdate
from domain.user.user_schema import PasswordUpdate

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user",
)

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(
        _user_create: user_schema.UserCreate,
        db: Session = Depends(get_db)
):
    if user_crud.is_username_exists(db, _user_create.username):
        raise HTTPException(status_code=409, detail="이미 사용 중인 아이디입니다.")
    if user_crud.is_email_exists(db, _user_create.email):
        raise HTTPException(status_code=409, detail="이미 등록된 이메일입니다.")
    if user_crud.is_phone_exists(db, _user_create.phone_number):
        raise HTTPException(status_code=409, detail="이미 등록된 전화번호입니다.")

    user_crud.create_user(db=db, user_create=_user_create)


@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = user_crud.get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="가입되지 않은 아이디입니다."
        )

    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비밀번호가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_crud.update_login_info(db, user)

    data = {
        "sub": str(user.id),
        "exp": datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_crud.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    return user

@router.post("/verify-password", status_code=204)
def verify_password(
        data: PasswordVerify,
        db: Session = Depends(get_db),
        current_user: ModelUser = Depends(get_current_user)
):
    if not user_crud.verify_user_password(db, current_user.id, data.password):
        raise HTTPException(
            status_code=400,
            detail="비밀번호가 일치하지 않습니다."
        )

@router.delete("/delete", status_code=204)
def delete_current_user(
        db: Session = Depends(get_db),
        current_user: ModelUser = Depends(get_current_user)
):
    user_crud.delete_user(db, current_user.id)

@router.get("/me", response_model=user_schema.User)
def get_current_user_info(current_user: ModelUser = Depends(get_current_user)):
    return current_user

@router.put("/user-update", status_code=204)
def update_user(
        data: UserUpdate,
        db: Session = Depends(get_db),
        current_user: ModelUser = Depends(get_current_user)
):
    user_crud.update_user_info(db, current_user, data)

@router.put("/update-password", status_code=204)
def update_password(
        data: PasswordUpdate,
        db: Session = Depends(get_db),
        current_user: ModelUser = Depends(get_current_user)
):
    user_crud.update_password(db, current_user, data.password)
