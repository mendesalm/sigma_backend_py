# backend_python/schemas/presenca_sessao_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PresencaSessaoBase(BaseModel):
    id_membro: Optional[int] = None
    id_visitante: Optional[int] = None
    status_presenca: str
    data_hora_checkin: Optional[datetime] = None

class PresencaSessaoCreate(PresencaSessaoBase):
    id_sessao: int

class PresencaSessao(PresencaSessaoBase):
    id: int
    id_sessao: int

    class Config:
        orm_mode = True
