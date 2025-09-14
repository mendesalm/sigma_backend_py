# backend_python/controllers/global/role_permission_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.role_permission_schema import RolePermissionCreate
from schemas.permission_schema import PermissionResponse
from schemas.role_schema import RoleResponse
from services import role_permission_service

router = APIRouter()

@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED, 
    summary="Atribui uma permissão a um cargo"
)
async def atribuir_permissao_a_cargo(
    dados: RolePermissionCreate, 
    db: Session = Depends(get_db)
):
    """Atribui uma permissão a um cargo."""
    return role_permission_service.atribuir_permissao_a_cargo(db=db, role_id=dados.role_id, permission_id=dados.permission_id)

@router.delete(
    "/", 
    status_code=status.HTTP_200_OK, 
    summary="Remove uma permissão de um cargo"
)
async def remover_permissao_de_cargo(
    dados: RolePermissionCreate, 
    db: Session = Depends(get_db)
):
    """Remove uma permissão de um cargo."""
    return role_permission_service.remover_permissao_de_cargo(db=db, role_id=dados.role_id, permission_id=dados.permission_id)

@router.get(
    "/roles/{role_id}/permissions", 
    response_model=List[PermissionResponse], 
    summary="Obtém todas as permissões de um cargo"
)
async def obter_permissoes_por_cargo(
    role_id: int, 
    db: Session = Depends(get_db)
):
    """Retorna todas as permissões associadas a um cargo."""
    return role_permission_service.obter_permissoes_por_cargo(db=db, role_id=role_id)

@router.get(
    "/permissions/{permission_id}/roles", 
    response_model=List[RoleResponse], 
    summary="Obtém todos os cargos que possuem uma permissão"
)
async def obter_cargos_por_permissao(
    permission_id: int, 
    db: Session = Depends(get_db)
):
    """Retorna todos os cargos que possuem uma permissão específica."""
    return role_permission_service.obter_cargos_por_permissao(db=db, permission_id=permission_id)