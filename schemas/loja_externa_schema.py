# backend_python/schemas/loja_externa_schema.py

from pydantic import BaseModel
from typing import Optional

class LojaExternaBase(BaseModel):
    nome: str
    numero: Optional[int] = None
    obediencia: Optional[str] = None

class LojaExternaCreate(LojaExternaBase):
    pass

class LojaExterna(LojaExternaBase):
    id: int

    class Config:
        orm_mode = True