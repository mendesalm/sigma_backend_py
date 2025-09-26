# backend_python/schemas/lodge_class_schema.py

from pydantic import BaseModel, Field
from typing import Optional

# Propriedades básicas compartilhadas
class LodgeClassBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100, description="Nome da Classe (Potência)")
    descricao: Optional[str] = Field(None, max_length=255, description="Descrição da Classe")

# Schema para a criação de uma Classe
class LodgeClassCreate(LodgeClassBase):
    pass

# Schema para a atualização de uma Classe
class LodgeClassUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    descricao: Optional[str] = Field(None, max_length=255)

# Schema para a resposta da API (visualização)
class LodgeClassResponse(LodgeClassBase):
    id: int

    class Config:
        from_attributes = True