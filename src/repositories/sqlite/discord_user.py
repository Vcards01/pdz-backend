from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.entities.discord_user import DiscordUserComplete
from src.repositories.sqlite.models.discord_user import DiscordUser as DiscordUserDB
from src.repositories.sqlite import get_session
from fastapi import Depends


class DiscordUserDAO:

    @classmethod
    def from_db(cls, discord_user: DiscordUserDB) -> DiscordUserComplete:

        return DiscordUserComplete(
            username=discord_user.username
        )


class DiscordUserRepository:
    """Repositorio de Usuario"""

    class UserNotFound(Exception):
        """Usuario solicitado não existe"""
    
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    async def create_discord_user(
        self, username: str
    ) -> DiscordUserComplete:
        """
        Cria um novo usuario no banco.

        Parameters:
            - username (str): Username do usuario.

        Returns:
            new_user (UserComplete): Novo usuário criado.
        """
        new_discord_user = DiscordUserDB(
            username=username,
        )
        self.db.add(new_discord_user)
        await self.db.commit()

        return DiscordUserDAO.from_db(new_discord_user)
    

    async def get_discord_user_by_name(self, username: str) -> DiscordUserComplete:
        """
        Retorna o usuario do discord com username informado.

        Parameters:
            - username (str): Username do usuario.

        Returns:
            user (UserComplete): Usuário encontrado.
        """
        async with self.db as session:
            query = select(DiscordUserDB).filter(DiscordUserDB.username == username.strip())
            result = await session.execute(query)
            user: DiscordUserDB = result.scalars().one_or_none()
            if user:
                return DiscordUserDAO.from_db(user)
            raise self.UserNotFound(username)