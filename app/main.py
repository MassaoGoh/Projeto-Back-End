from fastapi import FastAPI

app = FastAPI(
    title="Raízes do Nordeste API",
    description="API Back-end da rede Raízes do Nordeste",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Raízes do Nordeste API funcionando"
    }