from sqlalchemy import Column, Integer, String
from src.repositories.sqlite import Base


class DiscordUser(Base):
    __tablename__ = "discord_user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
