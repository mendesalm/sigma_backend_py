from contextlib import asynccontextmanager
from fastapi import FastAPI

from database.connection import engine, Base
from config.settings import config
from utils.logger import logger

# Importação dos roteadores globais
from controllers.global_controllers import (
    super_admin_controller,
    lodge_class_controller,
    permission_controller,
    role_controller,
    tenant_controller,
    webmaster_controller,
    role_permission_controller,
    loja_externa_controller,
    visitante_controller,
    checkin_controller # Novo
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
app = FastAPI(
    title="API do Sistema Sigma",
    description="API para o Sistema de Gestão de Lojas Maçônicas (SiGMa).",
    lifespan=lifespan
)

# --- Configuração do CORS ---
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Inclusão de Roteadores Globais ---
app.include_router(super_admin_controller.router, prefix="/api/global/superadmins", tags=["Global - Super Admins"])
app.include_router(lodge_class_controller.router, prefix="/api/global/lodge-classes", tags=["Global - Classes de Loja"])
app.include_router(permission_controller.router, prefix="/api/global/permissions", tags=["Global - Permissões"])
app.include_router(role_controller.router, prefix="/api/global/roles", tags=["Global - Cargos"])
app.include_router(tenant_controller.router, prefix="/api/global/tenants", tags=["Global - Tenants (Lojas)"])
app.include_router(webmaster_controller.router, prefix="/webmasters", tags=["Webmasters"])
app.include_router(role_permission_controller.router, prefix="/associacoes_cargo_permissao", tags=["Associações Cargo-Permissão"])
app.include_router(loja_externa_controller.router, prefix="/api/global/lojas-externas", tags=["Global - Lojas Externas"])
app.include_router(visitante_controller.router, prefix="/api/global/visitantes", tags=["Global - Visitantes"])
app.include_router(checkin_controller.router, prefix="/api", tags=["Check-in"]) # Novo

# --- Inclusão de Roteadores de Tenant ---
app.include_router(auth_controller.router, prefix="/api/tenant/auth", tags=["Tenant - Autenticação"])
app.include_router(membro_controller.router, prefix="/api/tenant/membros", tags=["Tenant - Membros"])
app.include_router(familiar_controller.router, prefix="/api/tenant/familiares", tags=["Tenant - Familiares"])
app.include_router(condecoracao_controller.router, prefix="/api/tenant/condecoracoes", tags=["Tenant - Condecorações"])
app.include_router(historico_cargo_controller.router, prefix="/api/tenant/historico-cargos", tags=["Tenant - Histórico de Cargos"])
app.include_router(sessao_maconica_controller.router, prefix="/api/tenant/sessoes", tags=["Tenant - Sessões Maçônicas"])
app.include_router(presenca_sessao_controller.router, prefix="/api/tenant/presencas", tags=["Tenant - Presenças de Sessão"])
app.include_router(administrative_process_controller.router, prefix="/api/tenant/processos-administrativos", tags=["Tenant - Processos Administrativos"])
app.include_router(webmaster_role_controller.router, prefix="/api/tenant/webmaster/atribuicao-cargos", tags=["Tenant - Gerenciamento de Cargos do Webmaster"])


# --- Endpoint Raiz ---
@app.get("/", tags=["Geral"], summary="Verifica o status da API")
async def ler_raiz():
    """Endpoint principal que retorna uma mensagem de boas-vindas."""
    return {"mensagem": "Backend FastAPI para o SiGMa está operacional!"}