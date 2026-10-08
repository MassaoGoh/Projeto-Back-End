from fastapi import (
    APIRouter,
    Depends,
    status
)

from sqlalchemy.orm import Session

from app.application.services.pagamento_service import (
    processar_pagamento
)

from app.core.security import get_current_user
from app.domain.models.usuario import Usuario
from app.infrastructure.database import get_db
from app.schemas.pagamento import (
    PagamentoCreate,
    PagamentoResponse
)


router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)


@router.post(
    "",
    response_model=PagamentoResponse,
    status_code=status.HTTP_201_CREATED
)
def pagar(
    dados: PagamentoCreate,
    usuario: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    return processar_pagamento(
        dados,
        usuario,
        db
    )