
from fastapi import Depends
import jwt
import requests
from src.repositories.sqlite.discord_user import DiscordUserRepository
from src.entities.discord_user import DiscordUserComplete

from src.auth import ALGOTITHM, SECRETE_KEY
class DiscordUserService:
    """Casos de uso de Usuarios."""

    # Exceções
    class InvalidData(Exception):
        "Dados informados invalidos"

    class UserNotFound(Exception):
        "Usuario não encontrado"

    def __init__(
        self,
        user_repo: DiscordUserRepository = Depends(DiscordUserRepository),
    ):
        self.user_repo = user_repo
        """Repositorio de usuarios do discord"""

    async def create_user(self, username: str):
        """
        Cria um novo usuario no sistema.

        Parameters:
            - username (str): Username do usuario.

        Expected errors:
            - InvalidData: Dados informados invalidos.

        Returns:
            check (bool): Um booleano se a senha conferir ou não.
        """
        if not username:
            raise self.InvalidData()

        try:
            user = await self.user_repo.create_discord_user(
                username=username
            )
        except Exception as e:
            raise e
        return user
    
    async def get_user_by_username(self, username: str) -> DiscordUserComplete:
        """
        Retorna o usuario do username informado.

        Parameters:
            - username (str): Nome do usuario.

        Expected errors:
            - UserNotFound: Usuario não encontrado.

        Returns:
            User (DiscordUserComplete): Se o usuario existir.
        """

        try:
            user = await self.user_repo.get_discord_user_by_name(username=username)
        except self.user_repo.UserNotFound:
            raise self.UserNotFound(username)

        return DiscordUserComplete(username=user.username)
    
    def check_discord_token(self, token: str):
            payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGOTITHM])
            token: str = payload.get("access_token")
            url = 'https://discord.com/api/users/@me'
            headers = {
                'Authorization': f'Bearer {token}'
            }

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # lança uma exceção para códigos de status de erro
                return True  # o token é válido se a solicitação for bem-sucedida
            except requests.exceptions.HTTPError as err:
                print(err)
                return False  # o token é inválido se houver um erro ao fazer a solicitação