from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.enums import StatusPedido
from app.domain.models.estoque import Estoque
from app.domain.models.item_pedido import ItemPedido
from app.domain.models.pedido import Pedido
from app.domain.models.produto import Produto
from app.domain.models.unidade import Unidade
from app.domain.models.usuario import Usuario
from app.schemas.pedido import (
    ItemPedidoResponse,
    PedidoCreate,
    PedidoResponse
)


def montar_response(
    pedido: Pedido,
    db: Session
) -> PedidoResponse:

    itens = db.scalars(
        select(ItemPedido)
        .where(
            ItemPedido.pedido_id == pedido.id
        )
    ).all()

    itens_response = [
        ItemPedidoResponse(
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unitario=float(
                item.preco_unitario
            )
        )
        for item in itens
    ]

    return PedidoResponse(
        pedido_id=pedido.id,
        usuario_id=pedido.usuario_id,
        unidade_id=pedido.unidade_id,
        canal_pedido=pedido.canal_pedido,
        status=pedido.status,
        valor_total=float(
            pedido.valor_total
        ),
        criado_em=pedido.criado_em,
        itens=itens_response
    )


def criar_pedido(
        
    dados: PedidoCreate,
    usuario: Usuario,
    db: Session
) -> PedidoResponse:

    unidade = db.get(
        Unidade,
        dados.unidade_id
    )

    if unidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada."
        )

    if not unidade.ativa:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unidade está inativa."
        )


    quantidades: dict[int, int] = {}

    for item in dados.itens:
        quantidades[item.produto_id] = (
            quantidades.get(
                item.produto_id,
                0
            )
            + item.quantidade
        )

    itens_validados = []

    valor_total = Decimal("0.00")

    for produto_id, quantidade in quantidades.items():

        produto = db.get(
            Produto,
            produto_id
        )

        if produto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto {produto_id} não encontrado."
            )

        if not produto.ativo:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Produto {produto.nome} está inativo."
            )

        estoque = db.scalar(
            select(Estoque).where(
                Estoque.unidade_id == dados.unidade_id,
                Estoque.produto_id == produto.id
            )
        )

    

        if estoque is None or estoque.quantidade < quantidade:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Estoque insuficiente para o produto {produto.nome}."
            )


        valor_total += produto.preco * quantidade



        itens_validados.append(
            (
                produto,
                estoque,
                quantidade
            )
        )

    pedido = Pedido(
        usuario_id=usuario.id,
        unidade_id=dados.unidade_id,
        canal_pedido=dados.canal_pedido.value,
        status=StatusPedido.AGUARDANDO_PAGAMENTO.value,
        valor_total=valor_total
    )

    try:
        db.add(pedido)

        db.flush()

        for (
            produto,
            estoque,
            quantidade
        ) in itens_validados:

            item = ItemPedido(
                pedido_id=pedido.id,
                produto_id=produto.id,
                quantidade=quantidade,
                preco_unitario=produto.preco
            )

            db.add(item)

            estoque.quantidade -= quantidade


        db.commit()
        db.refresh(pedido)

    except Exception:
        db.rollback()
        raise

    return montar_response(
        pedido,
        db
    )

def listar_pedidos(
    db: Session,
    usuario: Usuario,
    canal: str | None = None,
    status_pedido: str | None = None
) -> list[PedidoResponse]:

    query = select(Pedido)

    if usuario.perfil != "ADMIN":
        query = query.where(
            Pedido.usuario_id == usuario.id
        )

    if canal is not None:
        query = query.where(
            Pedido.canal_pedido == canal
        )

    if status_pedido is not None:
        query = query.where(
            Pedido.status == status_pedido
        )

    pedidos = db.scalars(
        query.order_by(
            Pedido.id.desc()
        )
    ).all()

    return [
        montar_response(
            pedido,
            db
        )
        for pedido in pedidos
    ]

def buscar_pedido(
    pedido_id: int,
    usuario: Usuario,
    db: Session
) -> PedidoResponse:

    pedido = db.get(
        Pedido,
        pedido_id
    )

    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado."
        )

    if (
        usuario.perfil != "ADMIN"
        and pedido.usuario_id != usuario.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar este pedido."
        )

    return montar_response(
        pedido,
        db
    )