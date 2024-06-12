from typing import Union
from pydantic import BaseModel

class DiscordUserComplete(BaseModel):
    username: str