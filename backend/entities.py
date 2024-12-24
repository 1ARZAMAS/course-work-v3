from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    # Один тест -> много вопросов
    questions = relationship('Question', back_populates='test')


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    # Один вопрос -> много вариантов ответа
    answers = relationship('Answer', back_populates='question')

    # Связь с таблицей Test (многие -> один)
    test = relationship('Test', back_populates='questions')


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    # Связь с таблицей Question (многие -> один)
    question = relationship('Question', back_populates='answers')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Один пользователь -> много ответов
    user_answers = relationship('UserAnswer', back_populates='user')


class UserAnswer(Base):
    __tablename__ = 'user_answers'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    answer_id = Column(Integer, ForeignKey('answers.id'), nullable=False)
    answered_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    # Связи с таблицами
    user = relationship('User', back_populates='user_answers')
    question = relationship('Question')
    answer = relationship('Answer')

