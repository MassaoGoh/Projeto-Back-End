from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=6, max_length=100)


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str

    model_config = ConfigDict(from_attributes=True)