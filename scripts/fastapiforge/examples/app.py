from fastapi import FastAPI

from src.routes import router


app = FastAPI(title="Teste de api")
app.include_router(router)
