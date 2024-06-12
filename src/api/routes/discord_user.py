from fastapi import APIRouter, Depends, HTTPException, status
from src.entities.discord_user import DiscordUserComplete
from src.auth import oauth_2_scheme
from src.use_cases.discord_user import DiscordUserService
router = APIRouter()


@router.post("/create")
async def create_new_user(
    form_data: DiscordUserComplete, service: DiscordUserService = Depends(DiscordUserService)
):
    """Cria um novo usuário."""
    try:
        user = await service.create_user(
            username=form_data.username,
        )
    except Exception as e:
        raise e

    return {"message": "Usuario adicionado com sucesso", "username": user.username}


@router.post("/check_username")
async def create_new_user(
    form_data: DiscordUserComplete, token: str = Depends(oauth_2_scheme), service: DiscordUserService = Depends(DiscordUserService)
):
    """Busca um usuário."""
    print(form_data)
    if not service.check_discord_token(token=token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possivel validar suas credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        await service.get_user_by_username(
            username=form_data.username,
        )
    except Exception as e:
        raise e

    return {"accepted":True,"message": "Usuario autorizado"}