# backend_python/controllers/global/permission_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.permission_schema import PermissionCreate, PermissionUpdate, PermissionResponse
from services import permission_service
from middleware.authorize_middleware import get_current_user
from models.models import SuperAdministrador

router = APIRouter()

# Dependência para garantir que o usuário é um SuperAdmin
async def get_current_super_admin(current_user_data: dict = Depends(get_current_user)) -> SuperAdministrador:
    if current_user_data.get("perfil") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas Super Administradores podem realizar esta ação."
        )
    return current_user_data.get("user")

@router.post(
    "/", 
    response_model=PermissionResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Cria uma nova permissão"
)
async def criar_permissao(
    permissao: PermissionCreate, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Cria uma nova permissão com a ação e descrição fornecidas."""
    return permission_service.criar_permissao(db=db, permissao=permissao)

@router.get(
    "/", 
    response_model=List[PermissionResponse], 
    summary="Lista todas as permissões"
)
async def listar_permissoes(
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Retorna uma lista de todas as permissões cadastradas."""
    return permission_service.obter_todas_permissoes(db=db)

@router.get(
    "/{permissao_id}", 
    response_model=PermissionResponse, 
    summary="Obtém uma permissão pelo ID"
)
async def obter_permissao_por_id(
    permissao_id: int, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Retorna uma permissão específica pelo seu ID."""
    permissao = permission_service.obter_permissao_por_id(db=db, permissao_id=permissao_id)
    if not permissao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permissão não encontrada.")
    return permissao

@router.put(
    "/{permissao_id}", 
    response_model=PermissionResponse, 
    summary="Atualiza uma permissão"
)
async def atualizar_permissao(
    permissao_id: int, 
    permissao_atualizacao: PermissionUpdate, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Atualiza as informações de uma permissão existente."""
    return permission_service.atualizar_permissao(db=db, permissao_id=permissao_id, permissao_atualizacao=permissao_atualizacao)

@router.delete(
    "/{permissao_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta uma permissão"
)
async def deletar_permissao(
    permissao_id: int, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Deleta uma permissão pelo ID."""
    permission_service.deletar_permissao(db=db, permissao_id=permissao_id)
    return None
