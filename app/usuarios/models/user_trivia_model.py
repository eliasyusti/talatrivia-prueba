from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.settings.database import Base


class UserTrivia(Base):
    __tablename__ = "user_trivias"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trivia_id = Column(Integer, ForeignKey("trivias.id"), nullable=False)
    score = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)

    user = relationship("User", back_populates="user_trivias")
    trivia = relationship("Trivia", back_populates="user_trivias")
