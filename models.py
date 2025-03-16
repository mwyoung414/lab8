from sqlalchemy import String, Boolean, DateTime, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()

class Todo(Base):
    __tablename__ = "TODO"

    ID: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    TITLE: Mapped[str] = mapped_column(String(255), nullable=False)
    DESCRIPTION: Mapped[str] = mapped_column(String(255), nullable=False)
    DONE: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    DELETED: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __init__(self, id, title, description, done, deleted=False):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.deleted = deleted

    def __repr__(self):
        return f"<Todo(id='{self.id}', title='{self.title}', description='{self.description}', done='{self.done}', deleted='{self.deleted}')>"
    
class User(Base):
    __tablename__ = "USER"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    USERNAME: Mapped[str] = mapped_column(String(255), nullable=False)
    PASSWORD: Mapped[str] = mapped_column(String(255), nullable=False)
    EMAIL: Mapped[str] = mapped_column(String(255), nullable=False)
    CREATED_ON: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    def __init__(self, id, username, password, email, created_on):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.created_on = created_on

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}', password='{self.password}', email='{self.email}', created_on='{self.created_on}')>"