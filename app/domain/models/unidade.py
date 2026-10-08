from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class Unidade(Base):
    __tablename__ = "unidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    ativa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)