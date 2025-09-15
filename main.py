from contextlib import asynccontextmanager
from fastapi import FastAPI

from database.connection import engine, Base
from config.settings import config
from utils.logger import logger

# Importação dos roteadores globais
from controllers.global import (
    super_admin_controller,
    lodge_class_controller,
    permission_controller,
    role_controller,
    tenant_controller,
    webmaster_controller,
    role_permission_controller,
    loja_externa_controller,
    visitante_controller
)

# Importação dos roteadores de tenant
from controllers.tenant import (
    auth_controller,
    administrative_process_controller,
    membro_controller,
    webmaster_role_controller,
    familiar_controller,
    condecoracao_controller,
    historico_cargo_controller,
    sessao_maconica_controller,
    presenca_sessao_controller
)

# --- Ciclo de Vida da Aplicação (Lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Contexto de ciclo de vida para a aplicação FastAPI.
    Executa ações durante a inicialização e finalização.
    """
    logger.info("Iniciando a aplicação...")
    # O Alembic agora é a fonte da verdade para a estrutura do banco de dados.
    # A linha abaixo pode ser mantida para desenvolvimento inicial, mas não cria mais tabelas.
    # Base.metadata.create_all(bind=engine)
    logger.info("Aplicação iniciada. Banco de dados gerenciado pelo Alembic.")
    yield
    logger.info("Finalizando a aplicação...")

# --- Instância Principal do FastAPI ---
aplicacao = FastAPI(
    title="API do Sistema Sigma",
    description="API para o Sistema de Gestão de Lojas Maçônicas (SiGMa).",
    lifespan=lifespan
)

# --- Inclusão de Roteadores Globais ---
aplicacao.include_router(super_admin_controller.router, prefix="/api/global/superadmins", tags=["Global - Super Admins"])
aplicacao.include_router(lodge_class_controller.router, prefix="/api/global/lodge-classes", tags=["Global - Classes de Loja"])
aplicacao.include_router(permission_controller.router, prefix="/api/global/permissions", tags=["Global - Permissões"])
aplicacao.include_router(role_controller.router, prefix="/api/global/roles", tags=["Global - Cargos"])
aplicacao.include_router(tenant_controller.router, prefix="/api/global/tenants", tags=["Global - Tenants (Lojas)"])
aplicacao.include_router(webmaster_controller.router, prefix="/webmasters", tags=["Webmasters"])
aplicacao.include_router(role_permission_controller.router, prefix="/associacoes_cargo_permissao", tags=["Associações Cargo-Permissão"])
aplicacao.include_router(loja_externa_controller.router, prefix="/api/global/lojas-externas", tags=["Global - Lojas Externas"])
aplicacao.include_router(visitante_controller.router, prefix="/api/global/visitantes", tags=["Global - Visitantes"])

# --- Inclusão de Roteadores de Tenant ---
aplicacao.include_router(auth_controller.router, prefix="/api/tenant/auth", tags=["Tenant - Autenticação"])
aplicacao.include_router(membro_controller.router, prefix="/api/tenant/membros", tags=["Tenant - Membros"])
aplicacao.include_router(familiar_controller.router, prefix="/api/tenant/familiares", tags=["Tenant - Familiares"])
aplicacao.include_router(condecoracao_controller.router, prefix="/api/tenant/condecoracoes", tags=["Tenant - Condecorações"])
aplicacao.include_router(historico_cargo_controller.router, prefix="/api/tenant/historico-cargos", tags=["Tenant - Histórico de Cargos"])
aplicacao.include_router(sessao_maconica_controller.router, prefix="/api/tenant/sessoes", tags=["Tenant - Sessões Maçônicas"])
aplicacao.include_router(presenca_sessao_controller.router, prefix="/api/tenant/presencas", tags=["Tenant - Presenças de Sessão"])
aplicacao.include_router(administrative_process_controller.router, prefix="/api/tenant/processos-administrativos", tags=["Tenant - Processos Administrativos"])
aplicacao.include_router(webmaster_role_controller.router, prefix="/api/tenant/webmaster/atribuicao-cargos", tags=["Tenant - Gerenciamento de Cargos do Webmaster"])


# --- Endpoint Raiz ---
@aplicacao.get("/", tags=["Geral"], summary="Verifica o status da API")
async def ler_raiz():
    """Endpoint principal que retorna uma mensagem de boas-vindas."""
    return {"mensagem": "Backend FastAPI para o SiGMa está operacional!"}
