# backend_python/controllers/global/tenant_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.tenant_schema import TenantCreate, TenantUpdate, TenantResponse
from services import tenant_service
from middleware.authorize_middleware import get_current_user
from models.models import SuperAdministrador

router = APIRouter()

# Dependência para garantir que o usuário é um SuperAdmin
async def get_current_super_admin(current_user_data: dict = Depends(get_current_user)) -> SuperAdministrador:
    """
    Verifica se o usuário atual é um SuperAdmin e retorna o objeto do usuário.
    Levanta uma exceção HTTPException se o perfil não for 'super_admin'.
    """
    if current_user_data.get("perfil") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas Super Administradores podem realizar esta ação."
        )
    return current_user_data.get("user")


@router.post(
    "/", 
    response_model=TenantResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Cria uma nova loja (tenant)"
)
async def criar_loja(
    loja: TenantCreate, 
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Cria uma nova loja, incluindo seu webmaster inicial e associações hierárquicas."""
    return tenant_service.criar_loja(db=db, dados_loja=loja)

@router.get(
    "/", 
    response_model=List[TenantResponse], 
    summary="Lista todas as lojas (tenants)"
)
async def listar_lojas(
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Retorna uma lista de todas as lojas (tenants) cadastradas."""
    return tenant_service.obter_todas_lojas(db=db)

@router.get(
    "/{loja_id}", 
    response_model=TenantResponse, 
    summary="Obtém uma loja (tenant) pelo ID"
)
async def obter_loja_por_id(
    loja_id: int, 
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Retorna uma loja (tenant) específica pelo seu ID."""
    loja = tenant_service.obter_loja_por_id(db=db, loja_id=loja_id)
    if not loja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada.")
    return loja

@router.put(
    "/{loja_id}", 
    response_model=TenantResponse, 
    summary="Atualiza uma loja (tenant)"
)
async def atualizar_loja(
    loja_id: int, 
    loja_atualizacao: TenantUpdate, 
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Atualiza as informações de uma loja (tenant) existente."""
    return tenant_service.atualizar_loja(db=db, loja_id=loja_id, loja_atualizacao=loja_atualizacao)

@router.delete(
    "/{loja_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta uma loja (tenant)"
)
async def deletar_loja(
    loja_id: int, 
    db: Session = Depends(get_db),
    current_super_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Deleta uma loja (tenant) pelo ID."""
    tenant_service.deletar_loja(db=db, loja_id=loja_id)
    return None

@router.get("/{loja_id}/qr-code", summary="Gera um QR Code para a loja")
async def get_qr_code(loja_id: int, db: Session = Depends(get_db)):
    return tenant_service.generate_qr_code(db=db, loja_id=loja_id)