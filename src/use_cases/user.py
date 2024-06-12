from fastapi import Depends
import requests
from src.entities.user import User
from src.repositories.sqlite.user import UserRepository
from src.use_cases.authentication import AuthenticationService
from jose import JWTError, jwt
from src.entities.token import TokenData
from src.auth import ALGOTITHM, SECRETE_KEY


class UserService:
    """Casos de uso de Usuarios."""

    # Exceções
    class InvalidData(Exception):
        "Dados informados invalidos"

    class InvalidToken(Exception):
        "Token invalido"

    def __init__(
        self,
        user_repo: UserRepository = Depends(UserRepository),
        auth_service: AuthenticationService = Depends(AuthenticationService),
    ):
        self.user_repo = user_repo
        """Repositorio de usuarios"""
        self.auth_service = auth_service
        """Casos de uso de autenticação"""

    async def create_user(self, username: str, email: str, password: str):
        """
        Cria um novo usuario no sistema.

        Parameters:
            - username (str): Username do usuario.
            - email (str): email do usuario.
            - password (str): Senha sem criptografia.

        Expected errors:
            - InvalidData: Dados informados invalidos.

        Returns:
            check (bool): Um booleano se a senha conferir ou não.
        """
        if not username or not email or not password:
            raise self.InvalidData()

        hashed_password = self.auth_service.get_password_hash(password=password)
        try:
            user = await self.user_repo.create_user(
                username=username, email=email, password=hashed_password
            )
        except Exception as e:
            raise e
        return user

    async def get_user_by_token(self, token: str) -> User:
        """
        Retorna o usuario do token informado.

        Parameters:
            - token (str): Token do usuario.

        Expected errors:
            - InvalidData: Dados informados invalidos.
            - InvalidToken: Erro com o token.

        Returns:
            check (bool): Um booleano se a senha conferir ou não.
        """
        try:
            payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGOTITHM])
            username: str = payload.get("sub")
            if username is None:
                raise self.InvalidData(username)

            token_data = TokenData(username=username)

        except JWTError:
            raise self.InvalidToken(token)

        user = await self.user_repo.get_user_by_name(username=token_data.username)
        if user is None:
            raise self.InvalidToken(token)

        return User(username=user.username, email=user.email)