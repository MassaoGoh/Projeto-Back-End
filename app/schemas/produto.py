from pydantic import BaseModel, ConfigDict


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    ativo: bool

    model_config = ConfigDict(
        from_attributes=True
    )