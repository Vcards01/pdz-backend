from fastapi import APIRouter, Depends, HTTPException, status
from src.entities.user import User, UserComplete
from src.auth import oauth_2_scheme
from src.use_cases.user import UserService


router = APIRouter()


@router.post("/create")
async def create_new_user(
    form_data: UserComplete, service: UserService = Depends(UserService)
):
    """Cria um novo usuário."""
    try:
        user = await service.create_user(
            username=form_data.username,
            email=form_data.email,
            password=form_data.password,
        )
    except Exception as e:
        raise e

    return {"message": "Usuario criado com sucesso", "username": user.username}


@router.get("/me", response_model=User)
async def get_current_user(
    token: str = Depends(oauth_2_scheme),
    manager: UserService = Depends(UserService),
):
    """Retorna o usuario baseado no token"""
    try:
        user = await manager.get_user_by_token(token=token)
    except manager.InvalidToken:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possivel validar suas credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
