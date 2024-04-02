from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# 데이터베이스 구성
host = "db"
user = "fauser"
password = "abc123!"
dbname = "fastapi"
db_url = f"mysql+pymysql://{user}:{password}@{host}/{dbname}"
engine = create_engine(db_url)

# ORM을 위한 베이스 선언
Base = declarative_base()

# ORM 모델 정의
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120), unique=True)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"

# 세션 팩토리 생성
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI 라우트 정의
@app.get("/")
def index():
    return {"message": "Hello from fastapi x docker compose"}

@app.get("/users")
def users():
    users = Session().query(User).all()
    return [repr(user) for user in users]
