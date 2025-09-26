from typing import Any
from fastapi import APIRouter, status
from sqlalchemy import text

from src.connectors.db import get_session


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/healph-check")
def root() -> dict[str, dict[str, Any]]:
    return {
        "app": {"status": status.HTTP_200_OK},
        "db": {"status": 200 if get_session().scalar(text("SELECT 1")) else 500},
    }
