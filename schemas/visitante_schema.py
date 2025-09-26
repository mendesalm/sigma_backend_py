# backend_python/schemas/visitante_schema.py

from pydantic import BaseModel
from typing import Optional
from pydantic_settings import SettingsConfigDict

class VisitanteBase(BaseModel):
    nome_completo: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    cim: Optional[str] = None
    id_loja_externa: Optional[int] = None

class VisitanteCreate(VisitanteBase):
    pass

class Visitante(VisitanteBase):
    id: int

    model_config = SettingsConfigDict(from_attributes=True)
