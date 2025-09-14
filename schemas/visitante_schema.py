# backend_python/schemas/visitante_schema.py

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from .loja_externa_schema import LojaExternaResponse # Para aninhar na resposta

# Schema base com campos comuns do Visitante
class VisitanteBase(BaseModel):
    nome_completo: str = Field(..., max_length=255, description="Nome completo do visitante.")
    email: Optional[EmailStr] = Field(None, description="Email do visitante.")
    cim: Optional[str] = Field(None, max_length=20, description="CIM do visitante (se maçom).")
    id_loja_origem: Optional[int] = Field(None, description="ID da loja de origem do visitante (se aplicável).")

# Schema para criação de um novo Visitante
class VisitanteCreate(VisitanteBase):
    pass

# Schema para atualização de um Visitante (todos os campos são opcionais)
class VisitanteUpdate(VisitanteBase):
    nome_completo: Optional[str] = Field(None, max_length=255)

# Schema para resposta da API (inclui campos gerados pelo banco de dados e LojaExterna aninhada)
class VisitanteResponse(VisitanteBase):
    id: int
    loja_origem: Optional[LojaExternaResponse] = None # Aninha a loja de origem

    class Config:
        from_attributes = True
