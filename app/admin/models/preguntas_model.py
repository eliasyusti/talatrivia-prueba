from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.settings.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    difficulty_id = Column(Integer, ForeignKey("difficulties.id", ondelete="CASCADE"))
    difficulty = relationship("Difficulty")

    options = relationship(
        "Option", back_populates="question", cascade="all, delete-orphan"
    )


class Difficulty(Base):
    __tablename__ = "difficulties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
