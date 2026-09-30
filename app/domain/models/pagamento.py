#id pk
#pedido_id fk pedidos.id
#valor decimal
#status str
#criado_em datetime

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    status: Mapped[String] = mapped_column(String(30), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)