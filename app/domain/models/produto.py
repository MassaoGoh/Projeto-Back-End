from decimal import Decimal

from sqlalchemy import Integer, String, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)