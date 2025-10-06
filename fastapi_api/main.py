from fastapi import FastAPI
from database import Base, engine
from routers import tasks

# Cria as tabelas automaticamente no MySQL
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Todo MCP",
    version="1.0.0",
    description="API de tarefas usando MySQL, pronta para integração com MCP"
)

app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "API de tarefas com MySQL ativa!"}
