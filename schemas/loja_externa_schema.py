# backend_python/schemas/loja_externa_schema.py

from pydantic import BaseModel, Field
from typing import Optional

# Schema base com campos comuns da Loja Externa
class LojaExternaBase(BaseModel):
    nome_loja: str = Field(..., max_length=255, description="Nome da loja externa.")
    obediencia: Optional[str] = Field(None, max_length=255, description="Obediência da loja externa.")
    cidade: Optional[str] = Field(None, max_length=100, description="Cidade da loja externa.")
    pais: Optional[str] = Field(None, max_length=100, description="País da loja externa.")

# Schema para criação de uma nova Loja Externa
class LojaExternaCreate(LojaExternaBase):
    pass

# Schema para atualização de uma Loja Externa (todos os campos são opcionais)
class LojaExternaUpdate(LojaExternaBase):
    nome_loja: Optional[str] = Field(None, max_length=255)

# Schema para resposta da API (inclui campos gerados pelo banco de dados)
class LojaExternaResponse(LojaExternaBase):
    id: int

    class Config:
        from_attributes = True
