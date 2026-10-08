from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models.estoque import Estoque
from app.domain.models.produto import Produto
from app.domain.models.unidade import Unidade
from app.infrastructure.database import get_db
from app.schemas.produto import ProdutoResponse


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


@router.get(
    "",
    response_model=list[ProdutoResponse]
)
def listar_produtos(
    unidade_id: int | None = Query(
        default=None,
        alias="unidadeId",
        ge=1
    ),
    db: Session = Depends(get_db)
):
    if unidade_id is None:
        return db.scalars(
            select(Produto)
            .where(Produto.ativo.is_(True))
            .order_by(Produto.nome)
        ).all()

    unidade = db.get(
        Unidade,
        unidade_id
    )

    if unidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada."
        )

    produtos = db.scalars(
        select(Produto)
        .join(
            Estoque,
            Estoque.produto_id == Produto.id
        )
        .where(
            Estoque.unidade_id == unidade_id,
            Estoque.quantidade > 0,
            Produto.ativo.is_(True)
        )
        .order_by(Produto.nome)
    ).all()

    return produtos