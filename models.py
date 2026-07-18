from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[Optional[bool]] = mapped_column(default=True)
    role: Mapped[str] = mapped_column(String(30))

    todos: Mapped[List["Todos"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"Users(id={self.id!r}, "
            f"username={self.username!r}, "
            f"email={self.email!r})"
        )


class Todos(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(30))
    priority: Mapped[int] = mapped_column()
    complete: Mapped[Optional[bool]] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="todos")

    def __repr__(self) -> str:
        return f"Todos(id={self.id!r}, title={self.title!r}, description={self.description!r}, user_id={self.user_id})"
