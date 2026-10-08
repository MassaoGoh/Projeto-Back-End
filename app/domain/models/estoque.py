from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class Estoque(Base):
    __tablename__ = "estoques"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    unidade_id: Mapped[int] = mapped_column(
        ForeignKey("unidades.id"),
        nullable=False
    )

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id"),
        nullable=False
    )

    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    table_args = (
        UniqueConstraint("unidade_id", "produto_id"),
    )