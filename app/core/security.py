from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.core.config import settings
from app.domain.models.usuario import Usuario
from app.infrastructure.database import get_db

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Recebe uma senha em texto puro e retorna seu hash.
    """
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str
) -> bool:
    """
    Verifica se a senha informada corresponde ao hash armazenado.
    """
    return password_hash.verify(
        password,
        hashed_password
    )


def create_access_token(
    user_id: int,
    perfil: str
) -> str:
    """
    Cria um JWT contendo o ID e o perfil do usuário.
    """

    now = datetime.now(timezone.utc)

    expires_at = now + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "perfil": perfil,
        "iat": now,
        "exp": expires_at
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

    return token


bearer_scheme = HTTPBearer(
    auto_error=False
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Obtém o usuário atualmente autenticado através do JWT.
    """

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido.",
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )

        user_id = int(user_id)

    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    usuario = db.get(
        Usuario,
        user_id
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    return usuario

def require_admin(
    usuario: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Permite acesso somente para usuários com perfil ADMIN.
    """

    if usuario.perfil != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não possui permissão para esta operação."
        )

    return usuario