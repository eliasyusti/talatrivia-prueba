from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.settings.database import Base


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    trivia_id = Column(Integer, ForeignKey("trivias.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    selected_option_id = Column(Integer, ForeignKey("options.id", ondelete="CASCADE"))
    is_correct = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="user_answers")
    trivia = relationship("Trivia", back_populates="user_answers")
    question = relationship("Question")
    selected_option = relationship("Option")
