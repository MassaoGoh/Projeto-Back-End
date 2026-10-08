from sqlalchemy import select

from app.core.security import hash_password
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
            db.commit()

            print("Administrador criado.")

        else:
            print("Administrador já existe.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()