from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models.unidade import Unidade
from app.infrastructure.database import get_db
from app.schemas.unidade import UnidadeResponse


router = APIRouter(
    prefix="/unidades",
    tags=["Unidades"]
)


@router.get(
    "",
    response_model=list[UnidadeResponse]
)
def listar_unidades(
    db: Session = Depends(get_db)
):
    unidades = db.scalars(
        select(Unidade)
        .where(Unidade.ativa.is_(True))
        .order_by(Unidade.nome)
    ).all()

    return unidades