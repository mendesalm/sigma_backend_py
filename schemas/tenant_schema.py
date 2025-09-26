# backend_python/schemas/tenant_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import time
from enum import Enum

# Re-usando o schema de resposta da classe para aninhamento
from .lodge_class_schema import LodgeClassResponse

class DiaSessaoEnum(str, Enum):
    domingo = "Domingo"
    segunda = "Segunda-feira"
    terca = "Terça-feira"
    quarta = "Quarta-feira"
    quinta = "Quinta-feira"
    sexta = "Sexta-feira"
    sabado = "Sábado"

class PeriodicidadeEnum(str, Enum):
    semanal = "Semanal"
    quinzenal = "Quinzenal"
    mensal = "Mensal"

class TenantBase(BaseModel):
    nome_loja: str = Field(..., description="Nome da Loja (Tenant).")
    codigo_loja: str = Field(..., description="Código único para a Loja.")
    id_classe: int = Field(..., description="ID da Classe (Potência) à qual a loja pertence.")
    numero_loja: Optional[str] = None
    titulo_loja: Optional[str] = None
    obediencia_loja: Optional[str] = None
    dominio_personalizado: Optional[str] = None
    plano: Optional[str] = None
    limite_usuarios: Optional[int] = None
    esta_ativo: bool = True
    status: Optional[str] = None
    dia_sessoes: Optional[DiaSessaoEnum] = None
    periodicidade: Optional[PeriodicidadeEnum] = None
    hora_sessao: Optional[time] = None

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    nome_loja: Optional[str] = None
    id_classe: Optional[int] = None
    numero_loja: Optional[str] = None
    titulo_loja: Optional[str] = None
    obediencia_loja: Optional[str] = None
    dominio_personalizado: Optional[str] = None
    plano: Optional[str] = None
    limite_usuarios: Optional[int] = None
    esta_ativo: Optional[bool] = None
    status: Optional[str] = None
    dia_sessoes: Optional[DiaSessaoEnum] = None
    periodicidade: Optional[PeriodicidadeEnum] = None
    hora_sessao: Optional[time] = None

class TenantResponse(TenantBase):
    id: int
    classe: Optional[LodgeClassResponse] = None # Aninhar os dados da classe

    class Config:
        from_attributes = True