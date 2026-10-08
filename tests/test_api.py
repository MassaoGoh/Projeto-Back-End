from collections.abc import Generator
from decimal import Decimal
from typing import TypedDict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import hash_password
from app.domain.models.estoque import Estoque
from app.domain.models.produto import Produto
from app.domain.models.unidade import Unidade
from app.domain.models.usuario import Usuario
from app.infrastructure.database import Base, get_db
from app.main import app


class DadosSeed(TypedDict):
    cliente: Usuario
    unidade: Unidade
    produto: Produto


class PedidoCriado(TypedDict):
    pedidoId: int


@pytest.fixture
def test_db() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    def override_get_db() -> Generator[Session, None, None]:
        with testing_session_local() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    with testing_session_local() as session:
        yield session

    app.dependency_overrides.pop(get_db, None)
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def client(test_db: Session) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def senha_hash() -> str:
    return hash_password("Cliente@123")


@pytest.fixture
def seed_data(
    test_db: Session,
    senha_hash: str,
) -> DadosSeed:
    cliente = Usuario(
        nome="Cliente Teste",
        email="cliente@raizes.com",
        senha_hash=senha_hash,
        perfil="CLIENTE",
    )
    unidade = Unidade(nome="Raízes do Nordeste - Recife", ativa=True)
    produto = Produto(
        nome="Cuscuz",
        preco=Decimal("12.90"),
        ativo=True,
    )
    test_db.add_all([cliente, unidade, produto])
    test_db.flush()
    estoque = Estoque(
        unidade_id=unidade.id,
        produto_id=produto.id,
        quantidade=100,
    )
    test_db.add(estoque)
    test_db.commit()

    return {
        "cliente": cliente,
        "unidade": unidade,
        "produto": produto,
    }


def obter_token_cliente(client: TestClient) -> str:
    resposta = client.post(
        "/auth/login",
        json={
            "email": "cliente@raizes.com",
            "senha": "Cliente@123",
        },
    )
    assert resposta.status_code == 200
    return resposta.json()["access_token"]


def criar_pedido(
    client: TestClient,
    seed_data: DadosSeed,
) -> PedidoCriado:
    token = obter_token_cliente(client)
    resposta = client.post(
        "/pedidos",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "unidadeId": seed_data["unidade"].id,
            "canalPedido": "APP",
            "formaPagamento": "MOCK",
            "itens": [
                {
                    "produtoId": seed_data["produto"].id,
                    "quantidade": 2,
                }
            ],
        },
    )
    assert resposta.status_code == 201
    return resposta.json()


def test_T01_login_retorna_token_valido(
    client: TestClient,
    seed_data: DadosSeed,
) -> None:
    resposta = client.post(
        "/auth/login",
        json={
            "email": "cliente@raizes.com",
            "senha": "Cliente@123",
        },
    )

    assert resposta.status_code == 200
    assert resposta.json()["token_type"] == "bearer"
    assert resposta.json()["access_token"]


def test_T02_cliente_autenticado_consulta_proprio_perfil(
    client: TestClient,
    seed_data: DadosSeed,
) -> None:
    token = obter_token_cliente(client)
    resposta = client.get(
        "/usuarios/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json() == {
        "id": seed_data["cliente"].id,
        "nome": "Cliente Teste",
        "email": "cliente@raizes.com",
        "perfil": "CLIENTE",
    }


def test_T03_lista_produtos_ativos(
    client: TestClient,
    seed_data: DadosSeed,
) -> None:
    resposta = client.get("/produtos")

    assert resposta.status_code == 200
    assert resposta.json() == [
        {
            "id": seed_data["produto"].id,
            "nome": "Cuscuz",
            "preco": 12.9,
            "ativo": True,
        }
    ]


def test_T04_cadastra_usuario_cliente(
    client: TestClient,
    seed_data: DadosSeed,
) -> None:
    resposta = client.post(
        "/usuarios",
        json={
            "nome": "Novo Cliente",
            "email": "novo.cliente@exemplo.com",
            "senha": "Senha123",
        },
    )

    assert resposta.status_code == 201
    assert resposta.json()["email"] == "novo.cliente@exemplo.com"
    assert resposta.json()["perfil"] == "CLIENTE"
    assert "senha" not in resposta.json()


def test_T05_cria_pedido_e_calcula_total(
    client: TestClient,
    seed_data: DadosSeed,
) -> None:
    token = obter_token_cliente(client)
    resposta = client.post(
        "/pedidos",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "unidadeId": seed_data["unidade"].id,
            "canalPedido": "APP",
            "formaPagamento": "MOCK",
            "itens": [
                {
                    "produtoId": seed_data["produto"].id,
                    "quantidade": 2,
                }
            ],
        },
    )

    assert resposta.status_code == 201
    assert resposta.json()["status"] == "AGUARDANDO_PAGAMENTO"
    assert resposta.json()["valorTotal"] == 25.8
    assert resposta.json()["itens"] == [
        {
            "produtoId": seed_data["produto"].id,
            "quantidade": 2,
            "precoUnitario": 12.9,
        }
    ]


def test_T06_aprova_pagamento_do_proprio_pedido(
    client: TestClient,
    seed_data: DadosSeed,
) -> None:
    pedido = criar_pedido(client, seed_data)
    token = obter_token_cliente(client)
    resposta = client.post(
        "/pagamentos",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "pedidoId": pedido["pedidoId"],
            "resultado": "APROVADO",
        },
    )

    assert resposta.status_code == 201
    assert resposta.json()["status"] == "APROVADO"
    assert resposta.json()["statusPedido"] == "PAGO"
    assert resposta.json()["valor"] == 25.8


def test_T07_acesso_sem_token_retorna_401(
    client: TestClient,
    seed_data: DadosSeed,
) -> None:
    resposta = client.get("/usuarios/me")

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Autenticação necessária."


def test_T08_cliente_sem_permissao_admin_retorna_403(
    client: TestClient,
    seed_data: DadosSeed,
) -> None:
    token = obter_token_cliente(client)
    resposta = client.get(
        "/usuarios/admin/teste",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Você não possui permissão para esta operação."
    )


def test_T09_login_com_senha_incorreta_retorna_401(
    client: TestClient,
    seed_data: DadosSeed,
) -> None:
    resposta = client.post(
        "/auth/login",
        json={
            "email": "cliente@raizes.com",
            "senha": "senha-incorreta",
        },
    )

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "E-mail ou senha inválidos."


def test_T10_pedido_com_estoque_insuficiente_retorna_409(
    client: TestClient,
    seed_data: DadosSeed,
) -> None:
    token = obter_token_cliente(client)
    resposta = client.post(
        "/pedidos",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "unidadeId": seed_data["unidade"].id,
            "canalPedido": "APP",
            "formaPagamento": "MOCK",
            "itens": [
                {
                    "produtoId": seed_data["produto"].id,
                    "quantidade": 101,
                }
            ],
        },
    )

    assert resposta.status_code == 409
    assert resposta.json()["detail"] == (
        "Estoque insuficiente para o produto Cuscuz."
    )
