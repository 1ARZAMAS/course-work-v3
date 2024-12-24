from pydantic import BaseModel
from typing import Optional, List

# ---------- TEST ----------

class TestCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TestResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True  # Это укажет Pydantic, что данные будут приходить как объекты SQLAlchemy


# ---------- QUESTION ----------

class QuestionCreate(BaseModel):
    text: str
    # Связь с тестом, это будет ID теста
    test_id: int

class QuestionResponse(BaseModel):
    id: int
    text: str
    test_id: int

    # Ответы, которые относятся к вопросу
    answers: List['AnswerResponse'] = []

    class Config:
        orm_mode = True


# ---------- ANSWER ----------

class AnswerCreate(BaseModel):
    text: str
    is_correct: bool
    question_id: int

class AnswerResponse(BaseModel):
    id: int
    text: str
    is_correct: bool
    question_id: int

    class Config:
        orm_mode = True


# ---------- USER ANSWER (Ответ пользователя на вопрос) ----------

class UserAnswerCreate(BaseModel):
    user_id: int
    question_id: int
    answer_id: int

class UserAnswerResponse(BaseModel):
    id: int
    user_id: int
    question_id: int
    answer_id: int
    answered_at: Optional[str] = None  # Время, когда был дан ответ

    class Config:
        orm_mode = True


# ---------- USER ----------

class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # Роль пользователя приходит строкой

class UserResponse(BaseModel):
    id: int
    username: str
    role: str  # Роль будет возвращаться как строка

    class Config:
        orm_mode = True
