from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    verify_password
)
from app.domain.models.usuario import Usuario
from app.infrastructure.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):
    usuario = db.scalar(
        select(Usuario).where(
            Usuario.email == dados.email
        )
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    senha_valida = verify_password(
        dados.senha,
        usuario.senha_hash
    )

    if not senha_valida:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    token = create_access_token(
        user_id=usuario.id,
        perfil=usuario.perfil
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )