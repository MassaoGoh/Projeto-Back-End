from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.usuarios import router as usuarios_router
from app.api.unidades import router as unidades_router
from app.api.produtos import router as produtos_router
from app.api.pedidos import router as pedidos_router
from app.api.pagamentos import router as pagamentos_router
from app.core.logging_config import configure_logging
from app.core.error_handlers import register_exception_handlers

configure_logging()


app = FastAPI(
    title="Raízes do Nordeste API",
    description="API Back-end da rede Raízes do Nordeste",
    version="1.0.0"
)

register_exception_handlers(app)

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
