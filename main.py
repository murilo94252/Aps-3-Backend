from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from database import criar_tabelas
from model import evento, participante, inscricao
from controller import (
    evento_controller,
    participante_controller,
    inscricao_controller,
    relatorio_controller,
)

criar_tabelas()

app = FastAPI(
    title="API de Gerenciamento de Eventos Acadêmicos",
    description="API REST com persistência em SQLite e relatórios consolidados",
    version="2.0.0",
)

app.include_router(evento_controller.router)
app.include_router(participante_controller.router)
app.include_router(inscricao_controller.router)
app.include_router(relatorio_controller.router)


@app.exception_handler(SQLAlchemyError)
def erro_de_banco(request: Request, erro: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Não foi possível concluir a operação. Tente novamente mais tarde."},
    )


@app.get("/")
def root():
    return {"mensagem": "API de Eventos Acadêmicos no ar. Acesse /docs para ver o Swagger."}
