# backend_python/schemas/loja_externa_schema.py

from pydantic import BaseModel
from typing import Optional
from pydantic_settings import SettingsConfigDict

class LojaExternaBase(BaseModel):
    nome: str
    numero: Optional[int] = None
    obediencia: Optional[str] = None

class LojaExternaCreate(LojaExternaBase):
    pass

class LojaExterna(LojaExternaBase):
    id: int

    model_config = SettingsConfigDict(from_attributes=True)