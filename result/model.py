from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from databases import Base

class Result(Base):

    __tablename__ = 'result'

    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    test_id:Mapped[int] = mapped_column(ForeignKey("test.id", ondelete='CASCADE'))
    point:Mapped[int]
    count_point:Mapped[int]
    title:Mapped[str]

