# backend_python/schemas/tenant_schema.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, time
from .potencia_schema import PotenciaResponse

class TenantBase(BaseModel):
    nome_loja: str = Field(..., description="Nome da Loja.")
    codigo_loja: str = Field(..., description="Código único da Loja.")
    id_potencia: int = Field(..., description="ID da Potência à qual a loja pertence.")
    data_fundacao: Optional[date] = None
    rito: Optional[str] = None
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
    # Outros campos de Loja
    esta_ativo: bool = True

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    # Todos os campos são opcionais na atualização
    nome_loja: Optional[str] = None
    id_potencia: Optional[int] = None
    # ... (etc)

class TenantResponse(TenantBase):
    id: int
    potencia: Optional[PotenciaResponse] = None
    class Config:
        from_attributes = True
