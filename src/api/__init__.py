from fastapi import APIRouter
from src.api.routes import authentication
from src.api.routes import user
from src.api.routes import discord_user
from src.api.routes import video_download

api_router = APIRouter()
api_router.include_router(
    authentication.router, prefix="/auth", tags=["Authentication"]
)
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(discord_user.router, prefix="/discord_user", tags=["Discord User"])
api_router.include_router(video_download.router, prefix="/videos", tags=["Ferramentas de video"])
