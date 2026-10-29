from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.orm import relationship
from database import Base


class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data = Column(Date, nullable=False)
    horario = Column(Time, nullable=False)
    local = Column(String, nullable=False)
    capacidade = Column(Integer, nullable=False)
    categoria = Column(String, nullable=False)

    inscricoes = relationship("Inscricao", back_populates="evento", cascade="all, delete-orphan")
