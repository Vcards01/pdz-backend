from typing import Union
from fastapi import Depends
from datetime import datetime, timedelta
from jose import jwt
import requests
from src.entities.user import User, UserComplete
from src.repositories.sqlite.user import UserRepository
from src.auth import pwd_context, ALGOTITHM, SECRETE_KEY


class AuthenticationService:
    """Casos de uso de Authenticação."""

    def __init__(self, user_repo: UserRepository = Depends(UserRepository)):
        self.user_repo = user_repo
        """Repositorio de usuarios"""

    # Funções de senha
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se a senha informada confere com o hash do usuario.

        Parameters:
            plain_password (str): Senha sem criptografia.
            hashed_password (str): Senha criptografada.

        Returns:
            check (bool): Um booleano se a senha conferir ou não.
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Cria um hash com a senha do usuario.

        Parameters:
            password (str): Senha sem criptografia.

        Returns:
            hashed_password (str) : A senha criptografada.
        """
        return pwd_context.hash(password)

    # Funções de token
    def create_access_token(
        self, data: dict, expires_delta: Union[timedelta, None] = None
    ):
        """
        Cria um token de acesso.

        Parameters:
            data (dict): Dados para gerar o token.
            expires_delta (Union[timedelta, None]): Tempo para expirar o token

        Returns:
            encoded_jwt (str) : Token.
        """

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGOTITHM)
        return encoded_jwt

    # Funções de autenticação
    async def authenticate_user(self, username: str, password: str) -> User:
        """
        Faz autenticação do usuario.

        Parameters:
            username (str): Username do usuario.
            password (str): Senha sem criptografia.

        Returns:
            user (User) : Obj to usuario authenticado.
        """
        user: UserComplete = await self.user_repo.get_user_by_name(username=username)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return User(username=user.username, email=user.email)


    