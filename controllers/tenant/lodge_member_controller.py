# backend_python/controllers/tenant/lodge_member_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.lodge_member_schema import LodgeMemberCreate, LodgeMemberUpdate, LodgeMemberResponse
from services import lodge_member_service
from middleware.tenant_middleware import get_current_tenant
from middleware.authorize_middleware import has_permission

router = APIRouter()

@router.post(
    "/", 
    response_model=LodgeMemberResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Cria um novo membro da loja"
)
async def criar_membro_loja(
    membro: LodgeMemberCreate, 
    db: Session = Depends(get_db),
    tenant: dict = Depends(get_current_tenant) # Garante que o tenant está no contexto
):
    """Cria um novo membro da loja para o tenant atual."""
    return lodge_member_service.criar_membro_loja(db=db, membro=membro, tenant_id=tenant.id)

@router.get(
    "/", 
    response_model=List[LodgeMemberResponse], 
    summary="Lista todos os membros da loja"
)
async def listar_membros_loja(
    db: Session = Depends(get_db),
    tenant: dict = Depends(get_current_tenant),
    current_user: dict = Depends(has_permission(['read:lodge_members'])) # Requer permissão
):
    """Retorna uma lista de todos os membros da loja para o tenant atual."""
    return lodge_member_service.obter_todos_membros_loja(db=db, tenant_id=tenant.id)

@router.get(
    "/{membro_id}", 
    response_model=LodgeMemberResponse, 
    summary="Obtém um membro da loja pelo ID"
)
async def obter_membro_loja_por_id(
    membro_id: int, 
    db: Session = Depends(get_db),
    tenant: dict = Depends(get_current_tenant),
    current_user: dict = Depends(has_permission(['read:lodge_members'])) # Requer permissão
):
    """Retorna um membro da loja específico pelo seu ID para o tenant atual."""
    return lodge_member_service.obter_membro_loja_por_id(db=db, membro_id=membro_id, tenant_id=tenant.id)

@router.put(
    "/{membro_id}", 
    response_model=LodgeMemberResponse, 
    summary="Atualiza um membro da loja"
)
async def atualizar_membro_loja(
    membro_id: int, 
    membro_atualizacao: LodgeMemberUpdate, 
    db: Session = Depends(get_db),
    tenant: dict = Depends(get_current_tenant),
    current_user: dict = Depends(has_permission(['update:lodge_members'])) # Requer permissão
):
    """Atualiza as informações de um membro da loja existente para o tenant atual."""
    return lodge_member_service.atualizar_membro_loja(db=db, membro_id=membro_id, tenant_id=tenant.id, membro_atualizacao=membro_atualizacao)

@router.delete(
    "/{membro_id}", 
    status_code=status.HTTP_200_OK, 
    summary="Deleta um membro da loja"
)
async def deletar_membro_loja(
    membro_id: int, 
    db: Session = Depends(get_db),
    tenant: dict = Depends(get_current_tenant),
    current_user: dict = Depends(has_permission(['delete:lodge_members'])) # Requer permissão
):
    """Deleta um membro da loja pelo ID para o tenant atual."""
    return lodge_member_service.deletar_membro_loja(db=db, membro_id=membro_id, tenant_id=tenant.id)
