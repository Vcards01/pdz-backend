from fastapi import Depends
from sqlalchemy import select
from src.repositories.sqlite import get_session
from src.entities.user import UserComplete
from src.repositories.sqlite.models.user import User as UserDB
from sqlalchemy.ext.asyncio import AsyncSession


class UserDAO:

    @classmethod
    def from_db(cls, user: UserDB) -> UserComplete:

        return UserComplete(
            username=user.username, email=user.email, password=user.password
        )


class UserRepository:
    """Repositorio de Usuario"""

    class UserNotFound(Exception):
        """Usuario solicitado não existe"""

    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    async def create_user(
        self, username: str, email: str, password: str
    ) -> UserComplete:
        """
        Cria um novo usuario no banco.

        Parameters:
            - username (str): Username do usuario.
            - email (str): email do usuario.
            - password (str): Senha sem criptografia.

        Returns:
            new_user (UserComplete): Novo usuário criado.
        """
        new_user = UserDB(
            username=username,
            email=email,
            password=password,
        )
        self.db.add(new_user)
        await self.db.commit()

        return UserDAO.from_db(new_user)

    async def get_user_by_name(self, username: str) -> UserComplete:
        """
        Retorna o usuario com username informado.

        Parameters:
            - username (str): Username do usuario.

        Returns:
            user (UserComplete): Usuário encontrado.
        """
        async with self.db as session:
            query = select(UserDB).filter(UserDB.username == username.strip())
            result = await session.execute(query)
            user: UserDB = result.scalars().one_or_none()
            if user:
                return UserDAO.from_db(user)
            raise self.UserNotFound(username)
