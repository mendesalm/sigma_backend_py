# backend_python/schemas/tenant_schema.py

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime, time

class TenantBase(BaseModel):
    codigo_loja: str = Field(..., min_length=3, max_length=32, description="Código único da loja.")
    numero_loja: Optional[str] = Field(None, max_length=255)
    nome_loja: Optional[str] = Field(None, max_length=255)
    titulo_loja: Optional[str] = Field(None, max_length=255)
    obediencia_loja: Optional[str] = Field(None, max_length=255)
    id_classe_loja: Optional[int] = Field(None, description="ID da classe de loja.")
    dominio_personalizado: Optional[str] = Field(None, max_length=255)
    plano: Optional[str] = Field("basic", max_length=255)
    limite_usuarios: Optional[int] = Field(20)
    configuracoes_globais: Optional[Dict[str, Any]] = Field({}, description="Configurações globais em formato JSON.")
    chaves_api: Optional[Dict[str, Any]] = Field({}, description="Chaves de API em formato JSON.")
    esta_ativo: Optional[bool] = Field(True)
    status: Optional[str] = Field(None, max_length=255)
    dia_sessoes: Optional[str] = Field(None, description="Dia da semana das sessões.")
    periodicidade: Optional[str] = Field(None, description="Periodicidade das sessões.")
    hora_sessao: Optional[time] = Field(None, description="Hora das sessões.")

class TenantCreate(TenantBase):
    # Para criação, o código da loja é obrigatório
    codigo_loja: str = Field(..., min_length=3, max_length=32, description="Código único da loja.")
    # Campos adicionais para o onboarding
    email_webmaster: EmailStr = Field(..., description="Email do webmaster inicial.")
    senha_webmaster: str = Field(..., min_length=8, description="Senha do webmaster inicial.")
    superior_lodges: Optional[List[int]] = Field([], description="Lista de IDs de lojas superiores na hierarquia.")

class TenantUpdate(TenantBase):
    # Todos os campos são opcionais para atualização
    codigo_loja: Optional[str] = Field(None, min_length=3, max_length=32, description="Código único da loja.")

class TenantResponse(TenantBase):
    id: int
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        from_attributes = True # Permite que o modelo seja criado a partir de atributos de objeto (ORM)
