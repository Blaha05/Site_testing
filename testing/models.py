from typing import Optional
from sqlalchemy import ForeignKey
from databases import Base
from sqlalchemy.orm import Mapped, mapped_column


class Test(Base):
    
    __tablename__ = 'test'
    

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    faculty:Mapped[Optional[str]]
    course:Mapped[Optional[str]]
    uset_id:Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))


class Question(Base):
    
    __tablename__ = 'question'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("test.id", ondelete='CASCADE'))
    text: Mapped[str]


class Answers(Base):
    
    __tablename__ = 'answer'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id", ondelete='CASCADE'))
    text: Mapped[str]
    status:Mapped[str]
