from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import CanalPedido, StatusPedido


class ItemPedidoCreate(BaseModel):
    produto_id: int = Field(
        alias="produtoId",
        gt=0
    )

    quantidade: int = Field(
        gt=0
    )

    model_config = ConfigDict(
        populate_by_name=True
    )


class PedidoCreate(BaseModel):
    unidade_id: int = Field(
        alias="unidadeId",
        gt=0
    )

    canal_pedido: CanalPedido = Field(
        alias="canalPedido"
    )

    itens: list[ItemPedidoCreate] = Field(
        min_length=1
    )

    forma_pagamento: Literal["MOCK"] = Field(
        alias="formaPagamento"
    )

    model_config = ConfigDict(
        populate_by_name=True
    )


class ItemPedidoResponse(BaseModel):
    produto_id: int = Field(
        alias="produtoId"
    )

    quantidade: int

    preco_unitario: float = Field(
        alias="precoUnitario"
    )

    model_config = ConfigDict(
        populate_by_name=True
    )


class PedidoResponse(BaseModel):
    pedido_id: int = Field(
        alias="pedidoId"
    )

    usuario_id: int = Field(
        alias="usuarioId"
    )

    unidade_id: int = Field(
        alias="unidadeId"
    )

    canal_pedido: str = Field(
        alias="canalPedido"
    )

    status: str

    valor_total: float = Field(
        alias="valorTotal"
    )

    criado_em: datetime = Field(
        alias="createdAt"
    )

    itens: list[ItemPedidoResponse]

    model_config = ConfigDict(
        populate_by_name=True
    )


class PedidoStatusUpdate(BaseModel):
    status: StatusPedido