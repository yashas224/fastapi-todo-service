from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database import Base


class Todos(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(30))
    priority: Mapped[int] = mapped_column()
    complete: Mapped[Optional[bool]] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"Todos(id={self.id!r}, title={self.title!r}, description={self.description!r})"
