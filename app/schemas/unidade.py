from pydantic import BaseModel, ConfigDict


class UnidadeResponse(BaseModel):
    id: int
    nome: str
    ativa: bool

    model_config = ConfigDict(
        from_attributes=True
    )