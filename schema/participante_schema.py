from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ParticipanteBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(..., min_length=1)
    email: EmailStr
    curso: str = Field(..., min_length=1)

    @field_validator("email")
    def email_em_minusculo(cls, valor):
        return valor.lower()


class ParticipanteCreate(ParticipanteBase):
    pass


class ParticipanteUpdate(ParticipanteBase):
    pass


class ParticipanteResponse(ParticipanteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
