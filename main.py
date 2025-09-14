from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.connection import engine, SessionLocal, Base, get_db
from models.models import SuperAdministrador, ClasseLoja, Loja, Webmaster
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from config.settings import config # Importa a configuração centralizada
from controllers.global import super_admin_controller # Importa o roteador de super_admin
from controllers.global import lodge_class_controller # Importa o roteador de classes de loja
from controllers.global import permission_controller # Importa o roteador de permissões
from controllers.global import role_controller # Importa o roteador de cargos
from controllers.global import tenant_controller # Importa o roteador de tenants
from controllers.global import webmaster_controller # Importa o roteador de webmasters
from controllers.global import role_permission_controller # Importa o roteador de associação de cargo e permissão
from controllers.tenant import auth_controller # Importa o roteador de autenticação de tenant
from controllers.tenant import administrative_process_controller # Importa o roteador de processos administrativos
from controllers.tenant import lodge_member_controller # Importa o roteador de membros da loja
from controllers.tenant import webmaster_role_controller # Importa o roteador de gerenciamento de cargos do webmaster
from utils.logger import logger # Importa o logger

# --- Configurações ---
SEGREDO_JWT = config.SEGREDO_JWT
ALGORITMO = config.ALGORITMO
MINUTOS_EXPIRACAO_TOKEN_ACESSO = config.MINUTOS_EXPIRACAO_TOKEN_ACESSO

# --- Ciclo de Vida da Aplicação (Lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Contexto de ciclo de vida para a aplicação FastAPI.
    Executa ações durante a inicialização e finalização.
    """
    logger.info("Iniciando a aplicação...")
    # Cria as tabelas no banco de dados (se não existirem)
    Base.metadata.create_all(bind=engine)
    logger.info("Tabelas do banco de dados verificadas/criadas.")
    yield
    logger.info("Finalizando a aplicação...")

# --- Instância Principal do FastAPI ---
aplicacao = FastAPI(
    title="API do Sistema Sigma",
    description="API para o Sistema de Gestão de Lojas Maçônicas (SiGMa).",
    lifespan=lifespan
)

# --- Inclusão de Roteadores ---
aplicacao.include_router(super_admin_controller.router, prefix="/api/global/superadmins", tags=["Global - Super Admins"])
aplicacao.include_router(lodge_class_controller.router, prefix="/api/global/lodge-classes", tags=["Global - Lodge Classes"])
aplicacao.include_router(permission_controller.router, prefix="/api/global/permissions", tags=["Global - Permissions"])
aplicacao.include_router(role_controller.router, prefix="/api/global/roles", tags=["Global - Roles"])
aplicacao.include_router(tenant_controller.router, prefix="/api/global/tenants", tags=["Global - Tenants"])
aplicacao.include_router(webmaster_controller.router, prefix="/webmasters", tags=["Webmasters"])
aplicacao.include_router(auth_controller.router, prefix="/tenant/auth", tags=["Tenant - Autenticação"])
aplicacao.include_router(administrative_process_controller.router, prefix="/tenant/administrative-processes", tags=["Tenant - Processos Administrativos"])
aplicacao.include_router(lodge_member_controller.router, prefix="/tenant/lodge-members", tags=["Tenant - Membros da Loja"])
aplicacao.include_router(webmaster_role_controller.router, prefix="/tenant/webmaster/role-assignments", tags=["Tenant - Gerenciamento de Cargos do Webmaster"])
aplicacao.include_router(role_permission_controller.router, prefix="/associacoes_cargo_permissao", tags=["Associações Cargo-Permissão"])

# --- Endpoints ---

@aplicacao.get("/", tags=["Geral"], summary="Verifica o status da API")
async def ler_raiz():
    """Endpoint principal que retorna uma mensagem de boas-vindas."""
    return {"mensagem": "Backend FastAPI para o SiGMa está operacional!"}
