from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Participante(Base):
    __tablename__ = "participantes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    curso = Column(String, nullable=False)

    inscricoes = relationship("Inscricao", back_populates="participante", cascade="all, delete-orphan")
