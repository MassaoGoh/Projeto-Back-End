import logging
from typing import Any


audit_logger = logging.getLogger("audit")


def audit_event(
    action: str,
    user_id: int | None = None,
    entity: str | None = None,
    entity_id: int | None = None,
    **details: Any
) -> None:

    details_text = " ".join(
        f"{key}={value}"
        for key, value in details.items()
    )

    audit_logger.info(
        "ACTION=%s USER_ID=%s ENTITY=%s ENTITY_ID=%s %s",
        action,
        user_id,
        entity,
        entity_id,
        details_text
    )