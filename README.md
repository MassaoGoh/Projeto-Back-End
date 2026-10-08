# Raízes do Nordeste API

Projeto acadêmico de faculdade: API backend do Raízes do Nordeste, desenvolvida com Python, FastAPI e SQLAlchemy.

A API oferece autenticação JWT, cadastro de usuários, consulta de unidades e produtos, criação e consulta de pedidos e processamento simulado de pagamentos.

## Visão geral

- Framework: FastAPI
- Banco de dados: SQLite
- ORM: SQLAlchemy
- Migrações: Alembic
- Autenticação: JWT com perfis `ADMIN` e `CLIENTE`
- Criptografia de senha: `pwdlib`
- Validação de dados: Pydantic
- Documentação automática: Swagger e Redoc

## Estrutura do projeto

```text
Projeto Back-end/
├── alembic/
│   └── versions/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── pagamentos.py
│   │   ├── pedidos.py
│   │   ├── produtos.py
│   │   ├── unidades.py
│   │   └── usuarios.py
│   ├── application/
│   │   └── services/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── domain/
│   │   ├── enums.py
│   │   └── models/
│   ├── infrastructure/
│   │   └── database.py
│   ├── schemas/
│   ├── main.py
│   └── seed.py
├── .env.example
├── alembic.ini
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.11+
- pip
- Ambiente virtual recomendado

## Configuração

1. Clone o repositório e acesse a pasta do projeto.
2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Copie `.env.example` para `.env` e defina uma chave secreta própria em `JWT_SECRET_KEY`. Não use uma chave de exemplo em produção:

```bash
copy .env.example .env
```

O arquivo `.env` deve conter:

```env
JWT_SECRET_KEY=troque-por-uma-chave-secreta
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Banco de dados e dados iniciais

O projeto usa SQLite no arquivo local `raizes.db`. Aplique as migrações antes de iniciar a API:

```bash
alembic upgrade head
```

Para criar os usuários de teste, a unidade, o estoque e os produtos iniciais:

```bash
python -m app.seed
```

O seed inclui estas credenciais para desenvolvimento local:

| Perfil | E-mail | Senha |
|---|---|---|
| Administrador | `admin@raizes.com` | `Admin123` |
| Cliente | `cliente@raizes.com` | `Cliente@123` |

Não use essas credenciais em produção.

O catálogo inicial inclui Cuscuz, Tapioca, Bolo de Macaxeira e Suco de Cajá, associados à unidade “Raízes do Nordeste - Recife”.

## Inicialização

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

- API: <http://127.0.0.1:8000>
- Swagger: <http://127.0.0.1:8000/docs>
- Redoc: <http://127.0.0.1:8000/redoc>

## Endpoints

Os exemplos usam JSON com nomes de campos em camelCase quando aplicável. Rotas marcadas como autenticadas exigem um token Bearer.

### Autenticação e usuários

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| `POST` | `/auth/login` | Público | Autentica e retorna um JWT |
| `POST` | `/usuarios` | Público | Cadastra um usuário com perfil `CLIENTE` |
| `GET` | `/usuarios/me` | Autenticado | Retorna os dados do usuário atual |
| `GET` | `/usuarios/admin/teste` | Administrador | Rota de teste de acesso administrativo |

Login:

```json
{
  "email": "cliente@raizes.com",
  "senha": "Cliente@123"
}
```

Resposta:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

Para chamar uma rota protegida, envie o JWT no cabeçalho HTTP `Authorization` usando o esquema `Bearer`.

### Unidades e produtos

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| `GET` | `/unidades` | Público | Lista unidades ativas |
| `GET` | `/produtos` | Público | Lista produtos ativos |
| `GET` | `/produtos?unidadeId=1` | Público | Lista produtos ativos com estoque disponível na unidade |

### Pedidos

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| `POST` | `/pedidos` | Autenticado | Cria um pedido |
| `GET` | `/pedidos` | Autenticado | Lista pedidos; clientes veem os próprios e administradores veem todos |
| `GET` | `/pedidos/{pedido_id}` | Autenticado | Consulta um pedido próprio ou, para administradores, qualquer pedido |

É possível filtrar a listagem por `canalPedido` e `status`, por exemplo:

```text
GET /pedidos?canalPedido=APP&status=AGUARDANDO_PAGAMENTO
```

Criação de pedido:

```json
{
  "unidadeId": 1,
  "canalPedido": "APP",
  "formaPagamento": "MOCK",
  "itens": [
    {
      "produtoId": 1,
      "quantidade": 2
    }
  ]
}
```

Os canais aceitos são `APP`, `TOTEM`, `BALCAO`, `PICKUP` e `WEB`. O pedido é criado com status `AGUARDANDO_PAGAMENTO`; a API valida unidade, produto e estoque, calcula o total com os preços atuais e reduz o estoque solicitado.

### Pagamentos

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| `POST` | `/pagamentos` | Autenticado | Registra uma tentativa de pagamento simulada |

Exemplo:

```json
{
  "pedidoId": 1,
  "resultado": "APROVADO"
}
```

`resultado` aceita `APROVADO` ou `NEGADO`. O usuário só pode pagar seus próprios pedidos; administradores podem pagar qualquer pedido. Um resultado aprovado altera o status do pedido para `PAGO`; um resultado negado altera para `PAGAMENTO_NEGADO`. `formaPagamento: "MOCK"` e esse resultado são simulações, não integração com um provedor de pagamentos real.

Os status possíveis de pedido incluem `AGUARDANDO_PAGAMENTO`, `PAGO`, `EM_PREPARO`, `PRONTO`, `ENTREGUE`, `CANCELADO` e `PAGAMENTO_NEGADO`.

## Licença

Este projeto foi criado para fins de desenvolvimento local e estudo de arquitetura de backend em FastAPI.
