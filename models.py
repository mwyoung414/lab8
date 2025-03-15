from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from db import Model

class Todo(Model):
    __tablename__ = "TODO"

    ID: Mapped[int] = mapped_column(primary_key=True)
    TITLE: Mapped[str] = mapped_column(String(255), nullable=False)
    DESCRIPTION: Mapped[str] = mapped_column(String(255), nullable=False)
    DONE: Mapped[bool] = mapped_column(Boolean, nullable=False)
    DELETED: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __init__(self, id, title, description, done, deleted=False):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.deleted = deleted

    def __repr__(self):
        return f"<Todo(id='{self.id}', title='{self.title}', description='{self.description}', done='{self.done}', deleted='{self.deleted}')>"