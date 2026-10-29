from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schema.participante_schema import ParticipanteCreate, ParticipanteUpdate, ParticipanteResponse
from service import participante_service

router = APIRouter(prefix="/participantes", tags=["Participantes"])


@router.post("", response_model=ParticipanteResponse, status_code=201)
def cadastrar_participante(participante: ParticipanteCreate, db: Session = Depends(get_db)):
    return participante_service.criar_participante(db, participante)


@router.get("", response_model=list[ParticipanteResponse])
def listar_participantes(db: Session = Depends(get_db)):
    return participante_service.listar_participantes(db)


@router.get("/{participante_id}", response_model=ParticipanteResponse)
def consultar_participante(participante_id: int, db: Session = Depends(get_db)):
    return participante_service.buscar_participante(db, participante_id)


@router.put("/{participante_id}", response_model=ParticipanteResponse)
def atualizar_participante(participante_id: int, participante: ParticipanteUpdate, db: Session = Depends(get_db)):
    return participante_service.atualizar_participante(db, participante_id, participante)


@router.delete("/{participante_id}", status_code=204)
def excluir_participante(participante_id: int, db: Session = Depends(get_db)):
    participante_service.excluir_participante(db, participante_id)
