# models.py
# 파이보 프로젝트는 ORM 을 지원하는 파이썬 데이터베이스 도구인 SQLAlchemy를 사용한다.
# SQLAlchemy는 모델 기반으로 데이터베이스를 처리한다.
# 모델 클래스들을 정의하는 파일

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(30), unique=True, nullable=False)

