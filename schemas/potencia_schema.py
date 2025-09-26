# backend_python/schemas/potencia_schema.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class PotenciaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    descricao: Optional[str] = Field(None, max_length=255)
    tipo: str
    id_potencia_superior: Optional[int] = None
    cnpj: Optional[str] = Field(None, max_length=18)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=20)
    site: Optional[str] = Field(None, max_length=255)
    logradouro: Optional[str] = Field(None, max_length=255)
    numero: Optional[str] = Field(None, max_length=20)
    complemento: Optional[str] = Field(None, max_length=100)
    bairro: Optional[str] = Field(None, max_length=100)
    cidade: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=2)
    cep: Optional[str] = Field(None, max_length=9)
    responsavel_tecnico_nome: Optional[str] = Field(None, max_length=255)
    responsavel_tecnico_email: Optional[EmailStr] = None

class PotenciaCreate(PotenciaBase):
    pass

class PotenciaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    # Adicionar todos os outros campos como opcionais
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    id_potencia_superior: Optional[int] = None
    cnpj: Optional[str] = None
    email: Optional[EmailStr] = None
    # ... etc

class PotenciaResponse(PotenciaBase):
    id: int
    class Config:
        from_attributes = True
