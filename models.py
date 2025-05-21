# models.py
# 파이보 프로젝트는 ORM 을 지원하는 파이썬 데이터베이스 도구인 SQLAlchemy를 사용한다.
# SQLAlchemy는 모델 기반으로 데이터베이스를 처리한다.
# 모델 클래스들을 정의하는 파일

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy import Enum as SqlEnum
import enum
from sqlalchemy.orm import relationship
from datetime import datetime

import pytz
seoul_tz = pytz.timezone("Asia/Seoul")

from database import Base

# Python Enum 정의
class GenderEnum(enum.Enum):
    male = "남"
    female = "여"

class TelecomEnum(enum.Enum):
    SKT = "SKT"
    KT = "KT"
    LGU = "LGU+"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True) # 내부 고유 ID
    name = Column(String(20), nullable=False) # 회원 이름
    username = Column(String(30), unique=True, nullable=False) # 로그인 ID
    password = Column(String(100), nullable=False) # 해시된 비밀번호
    email = Column(String(30), unique=True, nullable=False) # 이메일 주소
    telecom = Column(SqlEnum(TelecomEnum, name = "telecom_enum"), nullable=True)
    phone_number = Column(String(20), unique=True, nullable=True)
    birthdate = Column(Date, nullable=True)
    gender = Column(SqlEnum(GenderEnum, name="gender_enum"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(seoul_tz)) # 가입일
    last_login = Column(DateTime, nullable=True)
    login_count = Column(Integer, default=0)

