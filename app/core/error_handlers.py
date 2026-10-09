from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


ERROR_CODES = {
    400: "REQUISICAO_INVALIDA",
    401: "NAO_AUTENTICADO",
    403: "ACESSO_NEGADO",
    404: "RECURSO_NAO_ENCONTRADO",
    405: "METODO_NAO_PERMITIDO",
    409: "CONFLITO_REGRA_NEGOCIO",
    422: "DADOS_INVALIDOS",
    500: "ERRO_INTERNO",
}


def gerar_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def obter_codigo_erro(
    status_code: int,
) -> str:
    return ERROR_CODES.get(
        status_code,
        "ERRO_HTTP",
    )


def register_exception_handlers(
    app: FastAPI,
) -> None:

    # ========================================================
    # ERROS HTTP
    # ========================================================

    @app.exception_handler(
        StarletteHTTPException
    )
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ) -> JSONResponse:

        if isinstance(exc.detail, str):
            message = exc.detail
            details = []

        else:
            message = "Erro ao processar a requisição."
            details = exc.detail

        return JSONResponse(
            status_code=exc.status_code,
            headers=exc.headers,
            content={
                "error": obter_codigo_erro(
                    exc.status_code
                ),
                "message": message,
                "details": details,
                "timestamp": gerar_timestamp(),
                "path": request.url.path,
            },
        )

    # ========================================================
    # ERROS DE VALIDAÇÃO PYDANTIC / FASTAPI
    # ========================================================

    @app.exception_handler(
        RequestValidationError
    )
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:

        details = []

        for error in exc.errors():
            location = error.get(
                "loc",
                [],
            )

            # Remove "body", "query" etc.
            # para deixar o campo mais legível.
            field_parts = [
                str(part)
                for part in location
                if part not in {
                    "body",
                    "query",
                    "path",
                }
            ]

            field = ".".join(
                field_parts
            )

            details.append(
                {
                    "field": field,
                    "issue": error.get(
                        "msg",
                        "Valor inválido.",
                    ),
                }
            )

        return JSONResponse(
            status_code=422,
            content={
                "error": "DADOS_INVALIDOS",
                "message": (
                    "Um ou mais campos "
                    "possuem valores inválidos."
                ),
                "details": details,
                "timestamp": gerar_timestamp(),
                "path": request.url.path,
            },
        )

    # ========================================================
    # ERROS NÃO TRATADOS
    # ========================================================

    @app.exception_handler(
        Exception
    )
    async def generic_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=500,
            content={
                "error": "ERRO_INTERNO",
                "message": (
                    "Ocorreu um erro interno "
                    "no servidor."
                ),
                "details": [],
                "timestamp": gerar_timestamp(),
                "path": request.url.path,
            },
        )