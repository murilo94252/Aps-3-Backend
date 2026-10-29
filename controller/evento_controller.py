from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schema.evento_schema import EventoCreate, EventoUpdate, EventoResponse
from service import evento_service

router = APIRouter(prefix="/eventos", tags=["Eventos"])


@router.post("", response_model=EventoResponse, status_code=201)
def cadastrar_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    return evento_service.criar_evento(db, evento)


@router.get("", response_model=list[EventoResponse])
def listar_eventos(db: Session = Depends(get_db)):
    return evento_service.listar_eventos(db)


@router.get("/{evento_id}", response_model=EventoResponse)
def consultar_evento(evento_id: int, db: Session = Depends(get_db)):
    return evento_service.buscar_evento(db, evento_id)


@router.put("/{evento_id}", response_model=EventoResponse)
def atualizar_evento(evento_id: int, evento: EventoUpdate, db: Session = Depends(get_db)):
    return evento_service.atualizar_evento(db, evento_id, evento)


@router.delete("/{evento_id}", status_code=204)
def excluir_evento(evento_id: int, db: Session = Depends(get_db)):
    evento_service.excluir_evento(db, evento_id)
