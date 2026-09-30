from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    unidade_id: Mapped[int] = mapped_column(ForeignKey("unidades.id"), nullable=False)
    canal_pedido: Mapped[String] = mapped_column(String(20), nullable=False)
    status: Mapped[String] = mapped_column(String(30), nullable=False)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)