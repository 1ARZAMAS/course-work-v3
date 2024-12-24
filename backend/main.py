from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from typing import List
import logging

from database import SessionLocal, engine
import models
import schemas

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Константы для работы с JWT
SECRET_KEY = "your_secret_key"  # Поменяйте на более надежный
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Настройка криптографии для паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Инициализация FastAPI
app = FastAPI()

# Создаём таблицы в базе данных (если их нет)
models.Base.metadata.create_all(bind=engine)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Получение базы данных для работы
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание токена для авторизации
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Получение текущего пользователя из JWT токена
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.on_event("startup")
def startup_event():
    logger.info("Application started.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Application stopped.")

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Регистрация нового пользователя
@app.post("/register/", response_model=schemas.UserResponse)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    role_name = user_data.role
    role_obj = db.query(models.Role).filter(models.Role.name == role_name).first()
    if not role_obj:
        role_obj = models.Role(name=role_name)
        db.add(role_obj)
        db.flush()

    hashed_password = pwd_context.hash(user_data.password)
    new_user = models.User(
        username=user_data.username,
        hashed_password=hashed_password,
        role_id=role_obj.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Логин пользователя
@app.post("/login/")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    role_name = user.role_rel.name if user.role_rel else None
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role_name
    }

# Создание нового теста
@app.post("/tests/", response_model=schemas.TestResponse)
def create_test(test_data: schemas.TestCreate, db: Session = Depends(get_db)):
    db_test = models.Test(name=test_data.name, description=test_data.description)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

# Получение всех тестов
@app.get("/tests/", response_model=List[schemas.TestResponse])
def get_tests(db: Session = Depends(get_db)):
    tests = db.query(models.Test).all()
    return tests

# Создание нового вопроса
@app.post("/questions/", response_model=schemas.QuestionResponse)
def create_question(question_data: schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_question = models.Question(text=question_data.text, test_id=question_data.test_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# Получение вопросов по тесту
@app.get("/tests/{test_id}/questions", response_model=List[schemas.QuestionResponse])
def get_questions(test_id: int, db: Session = Depends(get_db)):
    questions = db.query(models.Question).filter(models.Question.test_id == test_id).all()
    return questions

# Создание нового ответа на вопрос
@app.post("/answers/", response_model=schemas.AnswerResponse)
def create_answer(answer_data: schemas.AnswerCreate, db: Session = Depends(get_db)):
    db_answer = models.Answer(
        text=answer_data.text, 
        is_correct=answer_data.is_correct, 
        question_id=answer_data.question_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

# Получение всех ответов для вопроса
@app.get("/questions/{question_id}/answers", response_model=List[schemas.AnswerResponse])
def get_answers(question_id: int, db: Session = Depends(get_db)):
    answers = db.query(models.Answer).filter(models.Answer.question_id == question_id).all()
    return answers

# Ответ пользователя на вопрос
@app.post("/user_answers/", response_model=schemas.UserAnswerResponse)
def create_user_answer(user_answer_data: schemas.UserAnswerCreate, db: Session = Depends(get_db)):
    db_user_answer = models.UserAnswer(
        user_id=user_answer_data.user_id,
        question_id=user_answer_data.question_id,
        answer_id=user_answer_data.answer_id
    )
    db.add(db_user_answer)
    db.commit()
    db.refresh(db_user_answer)
    return db_user_answer
