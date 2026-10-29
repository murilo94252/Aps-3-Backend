from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from model.participante import Participante
from schema.participante_schema import ParticipanteCreate, ParticipanteUpdate

MSG_EMAIL_DUPLICADO = "Já existe um participante cadastrado com este e-mail."


def criar_participante(db: Session, dados: ParticipanteCreate):
    participante = Participante(**dados.model_dump())
    db.add(participante)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=MSG_EMAIL_DUPLICADO)
    db.refresh(participante)
    return participante


def listar_participantes(db: Session):
    return db.query(Participante).order_by(Participante.id).all()


def buscar_participante(db: Session, participante_id: int):
    participante = db.get(Participante, participante_id)
    if participante is None:
        raise HTTPException(status_code=404, detail="Participante não encontrado.")
    return participante


def atualizar_participante(db: Session, participante_id: int, dados: ParticipanteUpdate):
    participante = buscar_participante(db, participante_id)

    for campo, valor in dados.model_dump().items():
        setattr(participante, campo, valor)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=MSG_EMAIL_DUPLICADO)
    db.refresh(participante)
    return participante


def excluir_participante(db: Session, participante_id: int):
    participante = buscar_participante(db, participante_id)
    db.delete(participante)
    db.commit()
