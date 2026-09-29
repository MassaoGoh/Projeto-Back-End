from enum import Enum


class PerfilUsuario(str, Enum):
    CLIENTE = "CLIENTE"
    ADMIN = "ADMIN"


class CanalPedido(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"


class StatusPedido(str, Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    PAGO = "PAGO"
    EM_PREPARO = "EM_PREPARO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"
    PAGAMENTO_NEGADO = "PAGAMENTO_NEGADO"


class StatusPagamento(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    NEGADO = "NEGADO"