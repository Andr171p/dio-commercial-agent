from sqlalchemy import Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class MessageOrm(Base):
    __tablename__ = "messages"

    chat_id: Mapped[str]
    role: Mapped[str]
    text: Mapped[str] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint("role IN ('user', 'ai')", name="check_role_values"),
    )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"role={self.role},\n"
            f"chat_id={self.chat_id},\n"
            f"text={self.text},\n"
            f"created_at={self.created_at}\n"
            f")"
        )

    def __repr__(self) -> str:
        return str(self)
