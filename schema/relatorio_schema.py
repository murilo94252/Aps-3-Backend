from pydantic import BaseModel


class OcupacaoEvento(BaseModel):
    evento_id: int
    titulo: str
    capacidade: int
    total_inscritos: int
    vagas_disponiveis: int
    percentual_ocupacao: float


class RelatorioCategoria(BaseModel):
    categoria: str
    total_eventos: int
    capacidade_total: int
    total_inscricoes: int


class RelatorioCurso(BaseModel):
    curso: str
    total_participantes: int
    total_inscricoes: int
