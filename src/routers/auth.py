import os
from typing import Any
from fastapi import APIRouter, Request, status
from sqlalchemy import text

from src.connectors.db import get_session


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/health-check")
def health_check(request: Request) -> dict[str, int] | int:
    if request.headers.get("api-gateway-request") == "True":
        if request.headers.get("api-gateway-token") == os.getenv("API_GATEWAY_TOKEN"):
            return {
                "app": status.HTTP_200_OK,
                "db": 200 if get_session().scalar(text("SELECT 1")) else 500
            }
        return status.HTTP_403_FORBIDDEN
    return status.HTTP_404_NOT_FOUND
