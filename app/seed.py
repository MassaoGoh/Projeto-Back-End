from decimal import Decimal

from sqlalchemy import select

from app.core.security import hash_password
from app.domain.models.estoque import Estoque
from app.domain.models.produto import Produto
from app.domain.models.unidade import Unidade
from app.domain.models.usuario import Usuario
from app.infrastructure.database import SessionLocal


def seed():
    db = SessionLocal()

    try:

        admin = db.scalar(
            select(Usuario).where(
                Usuario.email == "admin@raizes.com"
            )
        )

        if admin is None:
            admin = Usuario(
                nome="Administrador",
                email="admin@raizes.com",
                senha_hash=hash_password("Admin123"),
                perfil="ADMIN"
            )

            db.add(admin)


        cliente = db.scalar(
            select(Usuario).where(
                Usuario.email == "cliente@raizes.com"
            )
        )

        if cliente is None:
            cliente = Usuario(
                nome="Cliente Teste",
                email="cliente@raizes.com",
                senha_hash=hash_password("Cliente@123"),
                perfil="CLIENTE"
            )

            db.add(cliente)


        unidade = db.scalar(
            select(Unidade).where(
                Unidade.nome == "Raízes do Nordeste - Recife"
            )
        )

        if unidade is None:
            unidade = Unidade(
                nome="Raízes do Nordeste - Recife",
                ativa=True
            )

            db.add(unidade)
            db.flush()


        produtos_seed = [
            ("Cuscuz", Decimal("12.90"), 100),
            ("Tapioca", Decimal("15.90"), 100),
            ("Bolo de Macaxeira", Decimal("9.90"), 50),
            ("Suco de Cajá", Decimal("8.50"), 80),
        ]

        for nome, preco, quantidade in produtos_seed:

            produto = db.scalar(
                select(Produto).where(
                    Produto.nome == nome
                )
            )

            if produto is None:
                produto = Produto(
                    nome=nome,
                    preco=preco,
                    ativo=True
                )

                db.add(produto)
                db.flush()

            estoque = db.scalar(
                select(Estoque).where(
                    Estoque.unidade_id == unidade.id,
                    Estoque.produto_id == produto.id
                )
            )

            if estoque is None:
                estoque = Estoque(
                    unidade_id=unidade.id,
                    produto_id=produto.id,
                    quantidade=quantidade
                )

                db.add(estoque)

        db.commit()

        print("Seed executado com sucesso.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()