# backend_python/controllers/tenant/auth_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.auth_schema import LodgeMemberLogin, LodgeMemberSelectLodge, LodgeMemberForgotPassword, LodgeMemberResetPassword, LodgeMemberAuthResponse
from services import auth_service
from middleware.tenant_middleware import get_current_tenant
from middleware.authorize_middleware import get_current_user # Para refresh_token e select_lodge

router = APIRouter()

@router.post(
    "/login", 
    response_model=LodgeMemberAuthResponse, 
    summary="Autentica um membro da loja"
)
async def login_membro_loja(
    dados_login: LodgeMemberLogin, 
    db: Session = Depends(get_db),
    tenant: dict = Depends(get_current_tenant) # Garante que o tenant está no contexto
):
    """Autentica um membro da loja e retorna um token de acesso JWT."""
    # O tenant_id já está no contexto via get_current_tenant, pode ser usado no serviço se necessário
    return auth_service.login_membro_loja(db=db, dados_login=dados_login)

@router.post(
    "/select-lodge", 
    response_model=LodgeMemberAuthResponse, 
    summary="Permite que um membro selecione uma loja (se tiver múltiplas associações)"
)
async def selecionar_loja_membro(
    dados_selecao: LodgeMemberSelectLodge, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Requer autenticação prévia
):
    """Permite que um membro da loja selecione uma loja diferente se tiver múltiplas associações."""
    return auth_service.selecionar_loja_membro(db=db, dados_selecao=dados_selecao, current_user=current_user)

@router.post(
    "/refresh-token", 
    response_model=LodgeMemberAuthResponse, 
    summary="Atualiza o token de acesso de um membro da loja"
)
async def refresh_token(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Requer autenticação prévia
):
    """Gera um novo token de acesso para o usuário atual."""
    return auth_service.refresh_token(db=db, current_user=current_user)

@router.post(
    "/forgot-password", 
    status_code=status.HTTP_200_OK, 
    summary="Inicia o processo de recuperação de senha"
)
async def esqueci_senha(
    dados_esqueci_senha: LodgeMemberForgotPassword, 
    db: Session = Depends(get_db)
):
    """Inicia o processo de recuperação de senha para um membro da loja."""
    return auth_service.forgot_password(db=db, dados_esqueci_senha=dados_esqueci_senha)

@router.patch(
    "/reset-password", 
    status_code=status.HTTP_200_OK, 
    summary="Reseta a senha de um membro da loja"
)
async def resetar_senha(
    dados_reset_senha: LodgeMemberResetPassword, 
    db: Session = Depends(get_db)
):
    """Reseta a senha de um membro da loja usando um token de recuperação."""
    return auth_service.reset_password(db=db, dados_reset_senha=dados_reset_senha)
