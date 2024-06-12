from typing import Union
from pydantic import BaseModel

from src.entities.user import User


class Token(BaseModel):
    """Estrutura do token"""

    access_token: str
    token_type: str


class TokenResponse(Token):
    user: User

class TokenData(BaseModel):
    """Dados do token"""

    username: Union[str, None] = None
