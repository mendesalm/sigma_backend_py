# backend_python/schemas/presenca_sessao_schema.py

from pydantic import BaseModel
from typing import Optional

class PresencaSessaoBase(BaseModel):
    id_membro: int
    status_presenca: str

class PresencaSessaoCreate(PresencaSessaoBase):
    id_sessao: int

class PresencaSessao(PresencaSessaoBase):
    id: int
    id_sessao: int

    class Config:
        orm_mode = True