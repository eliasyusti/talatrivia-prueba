from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.settings.database import Base

# Tabla intermedia para la relación Many-to-Many entre Trivia y Questions
trivia_questions = Table(
    "trivia_questions",
    Base.metadata,
    Column(
        "trivia_id",
        Integer,
        ForeignKey("trivias.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "question_id",
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Trivia(Base):
    __tablename__ = "trivias"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relación Many-to-Many con preguntas
    questions = relationship(
        "Question", secondary=trivia_questions, back_populates="trivias"
    )

    # Relación con la asignación de trivias a usuarios
    user_assignments = relationship(
        "UserTriviaAssignment", back_populates="trivia", cascade="all, delete-orphan"
    )

    # Relación con respuestas y puntajes de usuarios
    user_answers = relationship("UserAnswer", back_populates="trivia")
    user_trivias = relationship("UserTrivia", back_populates="trivia")
