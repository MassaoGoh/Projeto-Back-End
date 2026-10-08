# Raízes do Nordeste API

API backend do projeto Raízes do Nordeste, desenvolvida com Python, FastAPI e SQLAlchemy.

A aplicação fornece autenticação via JWT, cadastro e consulta de usuários, além de uma base estrutural para expansão de módulos do negócio.

## Visão geral

- Framework: FastAPI
- Banco de dados: SQLite
- Autenticação: JWT com suporte a perfis de acesso
- Criptografia de senha: `pwdlib`
- Validação de dados: Pydantic
- Documentação automática: Swagger e Redoc

## Estrutura do projeto

```text
Projeto Back-end/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   └── usuarios.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── domain/
│   │   └── models/
│   ├── infrastructure/
│   │   └── database.py
│   ├── schemas/
│   ├── __init__.py
│   ├── main.py
│   └── seed.py
├── alembic/
├── .env.example
├── .gitignore
├── requirements.txt
├── raizes.db
└── README.md
```

## Requisitos

- Python 3.11+
- pip
- Ambiente virtual recomendado

## Configuração

1. Clone o repositório.
2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:

```bash
copy .env.example .env
```

Ou crie um arquivo `.env` com o conteúdo:

```env
JWT_SECRET_KEY=sua-chave-secreta
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Inicialização

### Rodar a aplicação

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

- http://127.0.0.1:8000
- Documentação Swagger: http://127.0.0.1:8000/docs
- Documentação Redoc: http://127.0.0.1:8000/redoc

### Popular usuário administrador

O projeto possui um seed para criar um usuário admin inicial:

```bash
python -m app.seed
```

Credenciais padrão:

- E-mail: `admin@raizes.com`
- Senha: `Admin123`

## Endpoints principais

### Autenticação

#### POST `/auth/login`

Realiza login e retorna um token JWT.

Exemplo de payload:

```json
{
  "email": "admin@raizes.com",
  "senha": "Admin123"
}
```

Resposta:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Usuários

#### POST `/usuarios`

Cria um novo usuário.

Exemplo de payload:

```json
{
  "nome": "Maria Silva",
  "email": "maria@email.com",
  "senha": "Senha123"
}
```

#### GET `/usuarios/me`

Retorna os dados do usuário autenticado.

Requer header:

```http
Authorization: Bearer <token>
```

#### GET `/usuarios/admin/teste`

Endpoint de teste para validação de acesso administrativo.

## Autenticação

Os endpoints protegidos exigem o header de autorização:

```http
Authorization: Bearer <token>
```

O token é gerado no login e contém:

- `sub`: ID do usuário
- `perfil`: perfil do usuário (ex.: `ADMIN`, `CLIENTE`)
- `exp`: data de expiração

## Banco de dados

O projeto usa SQLite com arquivo local:

```text
raizes.db
```

## Observações

- O projeto está estruturado em camadas (`api`, `core`, `domain`, `infrastructure`, `schemas`).
- A base do backend já contempla autenticação e gestão de usuários, com espaço para expansão de módulos do domínio do Raízes do Nordeste.
- Caso queira evoluir o projeto com migrations, o diretório `alembic/` está disponível para esse propósito.

## Licença

Este projeto foi criado para fins de desenvolvimento local e estudo de arquitetura de backend em FastAPI.
