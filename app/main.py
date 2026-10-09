from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.usuarios import router as usuarios_router
from app.api.unidades import router as unidades_router
from app.api.produtos import router as produtos_router
from app.api.pedidos import router as pedidos_router
from app.api.pagamentos import router as pagamentos_router



app = FastAPI(
    title="Raízes do Nordeste API",
    description="API Back-end da rede Raízes do Nordeste",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(unidades_router)
app.include_router(produtos_router)
app.include_router(pedidos_router)
app.include_router(pagamentos_router)

@app.get("/")
def home():
    return {
        "message": "Raízes do Nordeste API funcionando"
    }