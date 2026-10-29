from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from model.inscricao import Inscricao
from service.evento_service import buscar_evento
from service.participante_service import buscar_participante

MSG_JA_INSCRITO = "Participante já está inscrito neste evento."


def inscrever(db: Session, evento_id: int, participante_id: int):
    evento = buscar_evento(db, evento_id)
    participante = buscar_participante(db, participante_id)

    ja_inscrito = (
        db.query(Inscricao)
        .filter(Inscricao.evento_id == evento.id, Inscricao.participante_id == participante.id)
        .first()
    )
    if ja_inscrito:
        raise HTTPException(status_code=409, detail=MSG_JA_INSCRITO)

    total_inscritos = (
        db.query(func.count(Inscricao.id))
        .filter(Inscricao.evento_id == evento.id)
        .scalar()
    )
    if total_inscritos >= evento.capacidade:
        raise HTTPException(status_code=409, detail="Não existem vagas disponíveis para este evento.")

    inscricao = Inscricao(evento_id=evento.id, participante_id=participante.id)
    db.add(inscricao)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=MSG_JA_INSCRITO)
    db.refresh(inscricao)
    return inscricao


def listar_inscritos(db: Session, evento_id: int):
    evento = buscar_evento(db, evento_id)
    return [inscricao.participante for inscricao in evento.inscricoes]
