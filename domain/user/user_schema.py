from pydantic import BaseModel, field_validator, EmailStr, Field
from pydantic_core.core_schema import FieldValidationInfo
from datetime import datetime, date
from enum import Enum as PyEnum
import re

# 성별 Enum
class Gender(str, PyEnum):
    male = "남"
    female = "여"

# 통신사 Enum
class Telecom(str, PyEnum):
    SKT = "SKT"
    KT = "KT"
    LGU = "LGU+"


class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr
    name: str
    telecom: Telecom
    phone_number: str
    birthdate: date
    gender: Gender

    @field_validator('username',
                     'password1',
                     'password2',
                     'email',
                     'name',
                     'phone_number',
                     'birthdate',
                     'gender')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator("username")
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("아이디는 영문자와 숫자만 사용할 수 있습니다.")
        if len(v) < 4:
            raise ValueError("아이디는 최소 4자 이상이어야 합니다.")
        return v

    @field_validator("password1")
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError("비밀번호는 최소 6자 이상이어야 합니다.")
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        return v

    @field_validator('phone_number')
    def validate_phone_format(cls, v):
        pattern = r'^010-\d{4}-\d{4}$'
        if not re.match(pattern, v):
            raise ValueError("전화번호는 '010-0000-0000' 형식이어야 합니다.")
        return v

    @field_validator('birthdate')
    def validate_birthdate(cls, v):
        if v >= date.today():
            raise ValueError('생년월일은 오늘 이전 날짜여야 합니다.')
        return v


class PasswordVerify(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class User(BaseModel):
    id: int
    username: str
    email: str
    name: str
    telecom: Telecom | None = None
    phone_number: str | None = None
    birthdate: date | None = None
    gender: Gender | None = None
    created_at: datetime
    last_login: datetime | None = None
    login_count: int

    class Config:
        orm_mod = True # 이게 있어야 SQLAlchemy 객체도 변환됨

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    telecom: Telecom
    phone_number: str = Field(..., patternr=r"^010-\d{4}-\d{4}$")
    birthdate: date
    gender: Gender
