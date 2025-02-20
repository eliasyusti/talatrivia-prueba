from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.settings.database import Base
from app.admin.models.trivia_model import trivia_questions


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    # Relación con Trivia (Many-to-Many)
    trivias = relationship(
        "Trivia", secondary=trivia_questions, back_populates="questions"
    )

    # Relación con dificultad
    difficulty_id = Column(
        Integer, ForeignKey("difficulties.id", ondelete="CASCADE"), nullable=False
    )
    difficulty = relationship("Difficulty")

    # Relación con opciones
    options = relationship(
        "Option", back_populates="question", cascade="all, delete-orphan"
    )


class Difficulty(Base):
    __tablename__ = "difficulties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
