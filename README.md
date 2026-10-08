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

## Cenários de teste

Os testes automatizados da API usam `TestClient` e um banco SQLite em memória; não alteram `raizes.db` e não exigem a execução do seed real. Instale as dependências de desenvolvimento e execute:

```bash
pip install -r requirements-dev.txt
python -m pytest -v
```

Cada teste prepara cliente, unidade, produto e estoque próprios. As evidências abaixo indicam o teste identificável na saída de `pytest -v` e a operação que pode ser demonstrada no Swagger (`/docs`) com seu status e trecho de resposta.

### Cenários positivos — fluxo esperado

#### T01 — Login retorna token

- **Endpoint + método:** `POST /auth/login`
- **Pré-condição:** usuário `cliente@raizes.com` cadastrado.
- **Entrada (body):** `{"email":"cliente@raizes.com","senha":"Cliente@123"}`
- **Saída esperada:** `200 OK`; `{"access_token":"<JWT>","token_type":"bearer"}`
- **Evidência:** `tests/test_api.py::test_T01_login_retorna_token_valido` (`PASSED`); no Swagger, executar `POST /auth/login` e registrar o status e os campos da resposta.

#### T02 — Cliente consulta o próprio perfil

- **Endpoint + método:** `GET /usuarios/me`
- **Pré-condição:** cliente cadastrado e autenticado; usar o token retornado pelo login.
- **Entrada (header):** cabeçalho `Authorization` com token JWT válido; sem path, query ou body.
- **Saída esperada:** `200 OK`; `{"id":<id>,"nome":"Cliente Teste","email":"cliente@raizes.com","perfil":"CLIENTE"}`
- **Evidência:** `tests/test_api.py::test_T02_cliente_autenticado_consulta_proprio_perfil` (`PASSED`); no Swagger, autorizar com o JWT e executar `GET /usuarios/me`.

#### T03 — Lista produtos ativos

- **Endpoint + método:** `GET /produtos`
- **Pré-condição:** produto ativo Cuscuz cadastrado; endpoint público.
- **Entrada:** sem path, query ou body.
- **Saída esperada:** `200 OK`; lista contendo `{"nome":"Cuscuz","preco":12.9,"ativo":true}`.
- **Evidência:** `tests/test_api.py::test_T03_lista_produtos_ativos` (`PASSED`); no Swagger, executar `GET /produtos` e registrar o item retornado.

#### T04 — Cadastra usuário cliente

- **Endpoint + método:** `POST /usuarios`
- **Pré-condição:** e-mail ainda não cadastrado.
- **Entrada (body):** `{"nome":"Novo Cliente","email":"novo.cliente@exemplo.com","senha":"Senha123"}`
- **Saída esperada:** `201 Created`; resposta contém `"email":"novo.cliente@exemplo.com"` e `"perfil":"CLIENTE"`; não retorna a senha.
- **Evidência:** `tests/test_api.py::test_T04_cadastra_usuario_cliente` (`PASSED`); no Swagger, executar `POST /usuarios` e registrar status e campos públicos da resposta.

#### T05 — Cria pedido e calcula total

- **Endpoint + método:** `POST /pedidos`
- **Pré-condição:** cliente autenticado; unidade ativa e Cuscuz ativo com estoque de 100 unidades.
- **Entrada (header e body):** cabeçalho `Authorization` com token JWT válido; `{"unidadeId":<id>,"canalPedido":"APP","formaPagamento":"MOCK","itens":[{"produtoId":<id>,"quantidade":2}]}`
- **Saída esperada:** `201 Created`; resposta contém `"status":"AGUARDANDO_PAGAMENTO"`, `"valorTotal":25.8` e item com `"quantidade":2` e `"precoUnitario":12.9`.
- **Evidência:** `tests/test_api.py::test_T05_cria_pedido_e_calcula_total` (`PASSED`); no Swagger, executar `POST /pedidos` com IDs existentes e registrar status, total e itens.

#### T06 — Aprova pagamento do próprio pedido

- **Endpoint + método:** `POST /pagamentos`
- **Pré-condição:** cliente autenticado e proprietário de um pedido aguardando pagamento; o teste cria esse pedido antes de pagar.
- **Entrada (header e body):** cabeçalho `Authorization` com token JWT válido; `{"pedidoId":<id do pedido>,"resultado":"APROVADO"}`
- **Saída esperada:** `201 Created`; resposta contém `"status":"APROVADO"`, `"statusPedido":"PAGO"` e `"valor":25.8`.
- **Evidência:** `tests/test_api.py::test_T06_aprova_pagamento_do_proprio_pedido` (`PASSED`); no Swagger, criar um pedido e executar `POST /pagamentos` usando seu ID.

### Cenários negativos — erros e regras de negócio

#### T07 — Acesso sem token

- **Endpoint + método:** `GET /usuarios/me`
- **Pré-condição:** nenhuma; não enviar token.
- **Entrada:** sem path, query, body ou header `Authorization`.
- **Saída esperada:** `401 Unauthorized`; `{"detail":"Autenticação necessária."}`
- **Evidência:** `tests/test_api.py::test_T07_acesso_sem_token_retorna_401` (`PASSED`); no Swagger, executar `GET /usuarios/me` sem autorização.

#### T08 — Cliente tenta acessar recurso administrativo

- **Endpoint + método:** `GET /usuarios/admin/teste`
- **Pré-condição:** usuário autenticado com perfil `CLIENTE`.
- **Entrada (header):** cabeçalho `Authorization` com token JWT de usuário `CLIENTE`; sem path, query ou body.
- **Saída esperada:** `403 Forbidden`; `{"detail":"Você não possui permissão para esta operação."}`
- **Evidência:** `tests/test_api.py::test_T08_cliente_sem_permissao_admin_retorna_403` (`PASSED`); no Swagger, autorizar como cliente e executar `GET /usuarios/admin/teste`.

#### T09 — Login com senha incorreta

- **Endpoint + método:** `POST /auth/login`
- **Pré-condição:** usuário `cliente@raizes.com` cadastrado.
- **Entrada (body):** `{"email":"cliente@raizes.com","senha":"senha-incorreta"}`
- **Saída esperada:** `401 Unauthorized`; `{"detail":"E-mail ou senha inválidos."}`
- **Evidência:** `tests/test_api.py::test_T09_login_com_senha_incorreta_retorna_401` (`PASSED`); no Swagger, executar `POST /auth/login` com a senha inválida.

#### T10 — Pedido excede o estoque disponível

- **Endpoint + método:** `POST /pedidos`
- **Pré-condição:** cliente autenticado; unidade ativa e Cuscuz ativo com estoque de 100 unidades.
- **Entrada (header e body):** cabeçalho `Authorization` com token JWT válido; `{"unidadeId":<id>,"canalPedido":"APP","formaPagamento":"MOCK","itens":[{"produtoId":<id>,"quantidade":101}]}`
- **Saída esperada:** `409 Conflict`; `{"detail":"Estoque insuficiente para o produto Cuscuz."}`; pedido não é criado.
- **Evidência:** `tests/test_api.py::test_T10_pedido_com_estoque_insuficiente_retorna_409` (`PASSED`); no Swagger, executar `POST /pedidos` com quantidade acima do estoque.

## Licença

Este projeto foi criado para fins de desenvolvimento local e estudo de arquitetura de backend em FastAPI.
