from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.usuarios import router as usuarios_router


app = FastAPI(
    title="Raízes do Nordeste API",
    description="API Back-end da rede Raízes do Nordeste",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(usuarios_router)


@app.get("/")
def home():
    return {
        "message": "Raízes do Nordeste API funcionando"
    }