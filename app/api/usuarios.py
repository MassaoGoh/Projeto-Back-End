from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    get_current_user,
    hash_password,
    require_admin
)
from app.domain.models.usuario import Usuario
from app.infrastructure.database import get_db
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.post(
    "",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_usuario(
    dados: UsuarioCreate,
    db: Session = Depends(get_db)
):

    usuario_existente = db.scalar(
        select(Usuario).where(
            Usuario.email == dados.email
        )
    )

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado."
        )

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_password(dados.senha),
        perfil="CLIENTE"
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


@router.get(
    "/me",
    response_model=UsuarioResponse
)
def obter_meu_usuario(
    usuario: Usuario = Depends(get_current_user)
):
    return usuario


@router.get(
    "/admin/teste"
)
def testar_acesso_admin(
    usuario: Usuario = Depends(require_admin)
):
    return {
        "message": "Acesso administrativo autorizado.",
        "usuario": usuario.nome,
        "perfil": usuario.perfil
    }