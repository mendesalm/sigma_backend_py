# backend_python/schemas/super_admin_schema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Schema para o corpo da requisição de login
class SuperAdminLogin(BaseModel):
    email: EmailStr
    password: str  # RENOMEADO DE 'senha'

# Schema para a criação de um novo SuperAdmin
class SuperAdminCreate(BaseModel):
    nome_usuario: str = Field(..., min_length=3, description="Nome de usuário único para o super administrador.")
    email: EmailStr
    password: str = Field(..., min_length=8, description="Senha forte para o super administrador.") # RENOMEADO DE 'senha'

# Schema para a atualização de um SuperAdmin
class SuperAdminUpdate(BaseModel):
    nome_usuario: Optional[str] = Field(None, min_length=3, description="Novo nome de usuário.")
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, description="Nova senha (se for alterar).") # RENOMEADO DE 'senha'
    esta_ativo: Optional[bool] = None

# Schema para a resposta ao obter dados de um SuperAdmin (sem a senha)
class SuperAdminResponse(BaseModel):
    id: int
    nome_usuario: str
    email: EmailStr
    esta_ativo: bool

    class Config:
        from_attributes = True

# Schema para a resposta do token de acesso
class Token(BaseModel):
    token_de_acesso: str
    tipo_token: str = "bearer"