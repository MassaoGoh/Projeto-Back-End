from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domain.enums import (
    StatusPagamento,
    StatusPedido
)
from app.domain.models.pagamento import Pagamento
from app.domain.models.pedido import Pedido
from app.domain.models.usuario import Usuario
from app.schemas.pagamento import (
    PagamentoCreate,
    PagamentoResponse
)


def processar_pagamento(
    dados: PagamentoCreate,
    usuario: Usuario,
    db: Session
) -> PagamentoResponse:

    pedido = db.get(
        Pedido,
        dados.pedido_id
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
            detail="Sem permissão para pagar este pedido."
        )

    status_permitidos = {
        StatusPedido.AGUARDANDO_PAGAMENTO.value,
        StatusPedido.PAGAMENTO_NEGADO.value
    }

    if pedido.status not in status_permitidos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pedido não está aguardando pagamento."
        )

    if dados.resultado == "APROVADO":
        status_pagamento = (
            StatusPagamento.APROVADO.value
        )

        novo_status_pedido = (
            StatusPedido.PAGO.value
        )

    else:
        status_pagamento = (
            StatusPagamento.NEGADO.value
        )

        novo_status_pedido = (
            StatusPedido.PAGAMENTO_NEGADO.value
        )

    pagamento = Pagamento(
        pedido_id=pedido.id,
        valor=pedido.valor_total,
        status=status_pagamento
    )

    pedido.status = novo_status_pedido

    try:
        db.add(pagamento)
        db.commit()

        db.refresh(pagamento)
        db.refresh(pedido)

    except Exception:
        db.rollback()
        raise

    return PagamentoResponse(
        pagamento_id=pagamento.id,
        pedido_id=pedido.id,
        valor=float(pagamento.valor),
        status=pagamento.status,
        criado_em=pagamento.criado_em,
        status_pedido=pedido.status
    )