from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.settings.database import Base


class UserTriviaAssignment(Base):
    """📌 Modelo que representa la asignación de trivias a usuarios."""

    __tablename__ = "user_trivia_assignments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    trivia_id = Column(
        Integer, ForeignKey("trivias.id", ondelete="CASCADE"), nullable=False
    )

    # Restringe que un usuario no tenga la misma trivia asignada más de una vez
    __table_args__ = (
        UniqueConstraint("user_id", "trivia_id", name="unique_user_trivia"),
    )

    user = relationship("User", back_populates="trivia_assignments")
    trivia = relationship("Trivia", back_populates="user_assignments")
