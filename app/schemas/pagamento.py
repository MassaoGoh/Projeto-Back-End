from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PagamentoCreate(BaseModel):
    pedido_id: int = Field(
        alias="pedidoId",
        gt=0
    )

    resultado: Literal[
        "APROVADO",
        "NEGADO"
    ]

    model_config = ConfigDict(
        populate_by_name=True
    )


class PagamentoResponse(BaseModel):
    pagamento_id: int = Field(
        alias="pagamentoId"
    )

    pedido_id: int = Field(
        alias="pedidoId"
    )

    valor: float
    status: str

    criado_em: datetime = Field(
        alias="createdAt"
    )

    status_pedido: str = Field(
        alias="statusPedido"
    )

    model_config = ConfigDict(
        populate_by_name=True
    )