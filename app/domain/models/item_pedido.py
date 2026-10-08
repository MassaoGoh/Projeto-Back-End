#itens_pedido
#id pk
#pedido_id fk pedidos.id
#produto_id fk produtos.id
#quaantidade int 
#preco_unitario decimal

from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class Item_pedido(Base):
    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), nullable=False)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_unitario: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)