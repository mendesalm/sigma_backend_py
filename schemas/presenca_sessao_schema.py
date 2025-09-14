# backend_python/schemas/presenca_sessao_schema.py

from pydantic import BaseModel, Field, validator
from typing import Optional, Union
from datetime import datetime

from .membro_schema import MembroResponse
from .visitante_schema import VisitanteResponse

# Schema base com campos comuns da Presença na Sessão
class PresencaSessaoBase(BaseModel):
    id_sessao: int = Field(..., description="ID da sessão à qual a presença se refere.")
    id_membro: Optional[int] = Field(None, description="ID do membro presente (se for um membro da loja).")
    id_visitante: Optional[int] = Field(None, description="ID do visitante presente (se for um visitante).")

    @validator('id_membro', 'id_visitante')
    def check_one_of_membro_or_visitante(cls, v, values, field):
        if field.name == 'id_membro':
            if v is None and values.get('id_visitante') is None:
                raise ValueError('Pelo menos um entre id_membro ou id_visitante deve ser fornecido.')
            if v is not None and values.get('id_visitante') is not None:
                raise ValueError('Apenas um entre id_membro ou id_visitante deve ser fornecido.')
        return v

# Schema para criação de uma nova Presença na Sessão (manual)
class PresencaSessaoCreate(PresencaSessaoBase):
    pass

# Schema para resposta da API (inclui campos gerados pelo banco de dados e objetos aninhados)
class PresencaSessaoResponse(PresencaSessaoBase):
    id: int
    data_hora_checkin: datetime
    membro: Optional[MembroResponse] = None
    visitante: Optional[VisitanteResponse] = None

    class Config:
        from_attributes = True
