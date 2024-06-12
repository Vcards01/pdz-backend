from sqlalchemy import Column, Integer, String
from src.repositories.sqlite import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
