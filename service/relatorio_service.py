from sqlalchemy import func, distinct
from sqlalchemy.orm import Session
from model.evento import Evento
from model.inscricao import Inscricao
from model.participante import Participante


def ocupacao_eventos(db: Session):
    linhas = (
        db.query(Evento.id, Evento.titulo, Evento.capacidade, func.count(Inscricao.id))
        .outerjoin(Inscricao, Inscricao.evento_id == Evento.id)
        .group_by(Evento.id)
        .order_by(Evento.id)
        .all()
    )

    resultado = []
    for evento_id, titulo, capacidade, total_inscritos in linhas:
        if capacidade > 0:
            percentual = round(total_inscritos / capacidade * 100, 2)
        else:
            percentual = 0.0

        resultado.append({
            "evento_id": evento_id,
            "titulo": titulo,
            "capacidade": capacidade,
            "total_inscritos": total_inscritos,
            "vagas_disponiveis": capacidade - total_inscritos,
            "percentual_ocupacao": percentual,
        })
    return resultado


def eventos_por_categoria(db: Session):
    inscritos_por_evento = (
        db.query(Inscricao.evento_id, func.count(Inscricao.id).label("total"))
        .group_by(Inscricao.evento_id)
        .subquery()
    )

    linhas = (
        db.query(
            Evento.categoria,
            func.count(Evento.id),
            func.sum(Evento.capacidade),
            func.coalesce(func.sum(inscritos_por_evento.c.total), 0),
        )
        .outerjoin(inscritos_por_evento, inscritos_por_evento.c.evento_id == Evento.id)
        .group_by(Evento.categoria)
        .order_by(Evento.categoria)
        .all()
    )

    return [
        {
            "categoria": categoria,
            "total_eventos": total_eventos,
            "capacidade_total": capacidade_total,
            "total_inscricoes": total_inscricoes,
        }
        for categoria, total_eventos, capacidade_total, total_inscricoes in linhas
    ]


def participacao_por_curso(db: Session):
    linhas = (
        db.query(
            Participante.curso,
            func.count(distinct(Participante.id)),
            func.count(Inscricao.id),
        )
        .outerjoin(Inscricao, Inscricao.participante_id == Participante.id)
        .group_by(Participante.curso)
        .order_by(Participante.curso)
        .all()
    )

    return [
        {
            "curso": curso,
            "total_participantes": total_participantes,
            "total_inscricoes": total_inscricoes,
        }
        for curso, total_participantes, total_inscricoes in linhas
    ]
