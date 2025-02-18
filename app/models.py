from .database import Base
from sqlalchemy.sql.expression import null  # noqa: F401
from sqlalchemy import Column, Integer, String, Boolean


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)