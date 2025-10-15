from .base import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, ForeignKey
import datetime

class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now())
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, title={self.username!r}, author_id{self.author_id!r}"
        )