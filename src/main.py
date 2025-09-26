import os
import uvicorn

from fastapi import FastAPI

from src.routers.auth import router as auth_router

app = FastAPI(
    title="auth_service",
    version="0.0.1",
    debug=True if os.getenv("APP_DEBUG") == "True" else False,
)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
