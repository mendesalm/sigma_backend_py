# backend_python/controllers/tenant/webmaster_role_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.webmaster_role_schema import WebmasterRoleAssignment, WebmasterRoleResponse
from services import webmaster_role_service
from middleware.tenant_middleware import get_current_tenant
from middleware.authorize_middleware import has_permission

router = APIRouter()

@router.post(
    "/assign", 
    response_model=WebmasterRoleResponse, 
    status_code=status.HTTP_200_OK, 
    summary="Atribui um cargo a um membro da loja"
)
async def atribuir_cargo_a_membro_loja(
    assignment: WebmasterRoleAssignment, 
    db: Session = Depends(get_db),
    tenant: dict = Depends(get_current_tenant),
    current_user: dict = Depends(has_permission(['manage:roles'])) # Requer permissão
):
    """Atribui um cargo a um membro da loja através de sua associação."""
    return webmaster_role_service.atribuir_cargo_a_membro_loja(
        db=db, 
        associacao_id=assignment.lodge_member_association_id, 
        role_id=assignment.role_id
    )

@router.delete(
    "/remove", 
    response_model=WebmasterRoleResponse, 
    status_code=status.HTTP_200_OK, 
    summary="Remove um cargo de um membro da loja"
)
async def remover_cargo_de_membro_loja(
    assignment: WebmasterRoleAssignment, 
    db: Session = Depends(get_db),
    tenant: dict = Depends(get_current_tenant),
    current_user: dict = Depends(has_permission(['manage:roles'])) # Requer permissão
):
    """Remove o cargo de um membro da loja (definindo role_id como nulo, se permitido pelo schema)."""
    return webmaster_role_service.remover_cargo_de_membro_loja(db=db, associacao_id=assignment.lodge_member_association_id)

@router.get(
    "/{lodge_member_association_id}", 
    response_model=WebmasterRoleResponse, 
    summary="Obtém o cargo de um membro da loja"
)
async def obter_cargo_membro_loja(
    lodge_member_association_id: int, 
    db: Session = Depends(get_db),
    tenant: dict = Depends(get_current_tenant),
    current_user: dict = Depends(has_permission(['manage:roles'])) # Requer permissão
):
    """Obtém o cargo de um membro da loja através de sua associação."""
    return webmaster_role_service.obter_cargo_membro_loja(db=db, associacao_id=lodge_member_association_id)
