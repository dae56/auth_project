import os
import uvicorn

from fastapi import FastAPI
from sqlalchemy import text

from src.routers.auth import router as auth_router
from src.connectors.db import get_session

app = FastAPI(
    title='auth_service',
    version='0.0.1',
    debug=True if os.getenv('APP_DEBUG') == 'True' else False,
)
app.include_router(auth_router)

if __name__ == '__main__':
    print('{status: 200}' if get_session().scalar(text('SELECT 1')) == 1 else '{status: 500}')
    uvicorn.run(app, host='127.0.0.1', port=8000)


    # C:\Users\alexey\Desktop\auth_project\.venv\Scripts\python.exe C:\Users\alexey\Desktop\auth_project\src\main.py