from fastapi import HTTPException
from sqlalchemy.orm import Session
from model.evento import Evento
from schema.evento_schema import EventoCreate, EventoUpdate


def criar_evento(db: Session, dados: EventoCreate):
    evento = Evento(**dados.model_dump())
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento


def listar_eventos(db: Session):
    return db.query(Evento).order_by(Evento.id).all()


def buscar_evento(db: Session, evento_id: int):
    evento = db.get(Evento, evento_id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")
    return evento


def atualizar_evento(db: Session, evento_id: int, dados: EventoUpdate):
    evento = buscar_evento(db, evento_id)

    if dados.capacidade < len(evento.inscricoes):
        raise HTTPException(
            status_code=409,
            detail="A capacidade não pode ser menor que o número de inscritos.",
        )

    for campo, valor in dados.model_dump().items():
        setattr(evento, campo, valor)

    db.commit()
    db.refresh(evento)
    return evento


def excluir_evento(db: Session, evento_id: int):
    evento = buscar_evento(db, evento_id)
    db.delete(evento)
    db.commit()
