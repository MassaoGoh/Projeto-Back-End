from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from sqlalchemy.orm import Session

from app.application.services.pedido_service import (
    buscar_pedido,
    criar_pedido,
    listar_pedidos
)

from app.core.security import get_current_user
from app.domain.enums import CanalPedido, StatusPedido
from app.domain.models.usuario import Usuario
from app.infrastructure.database import get_db
from app.schemas.pedido import (
    PedidoCreate,
    PedidoResponse
)


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.post(
    "",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar(
    dados: PedidoCreate,
    usuario: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    return criar_pedido(
        dados,
        usuario,
        db
    )


@router.get(
    "",
    response_model=list[PedidoResponse]
)
def listar(
    canal: CanalPedido | None = Query(
        default=None,
        alias="canalPedido"
    ),
    status_pedido: StatusPedido | None = Query(
        default=None,
        alias="status"
    ),
    usuario: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    return listar_pedidos(
        db=db,
        usuario=usuario,
        canal=canal.value if canal else None,
        status_pedido=(
            status_pedido.value
            if status_pedido
            else None
        )
    )


@router.get(
    "/{pedido_id}",
    response_model=PedidoResponse
)
def buscar(
    pedido_id: int,
    usuario: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    return buscar_pedido(
        pedido_id,
        usuario,
        db
    )