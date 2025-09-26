# backend_python/controllers/tenant/webmaster_role_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.webmaster_role_schema import WebmasterRoleAssignment, WebmasterRoleResponse
from services import webmaster_role_service
# A função 'has_permission' não está implementada, então a importação e uso foram comentados.
from middleware.authorize_middleware import get_current_user #, has_permission

router = APIRouter()

@router.post("/assign", response_model=WebmasterRoleResponse, status_code=status.HTTP_201_CREATED)
def assign_role_to_webmaster(
    assignment: WebmasterRoleAssignment, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Proteção básica
    # has_access: bool = Depends(has_permission("assign_webmaster_role")) # TODO: Implementar
):
    return webmaster_role_service.assign_role(db=db, assignment=assignment)

@router.post("/unassign", status_code=status.HTTP_204_NO_CONTENT)
def unassign_role_from_webmaster(
    assignment: WebmasterRoleAssignment, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Proteção básica
    # has_access: bool = Depends(has_permission("unassign_webmaster_role")) # TODO: Implementar
):
    webmaster_role_service.unassign_role(db=db, assignment=assignment)
    return

@router.get("/{webmaster_id}/roles", response_model=List[WebmasterRoleResponse])
def get_webmaster_roles(
    webmaster_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Proteção básica
    # has_access: bool = Depends(has_permission("view_webmaster_roles")) # TODO: Implementar
):
    return webmaster_role_service.get_roles_for_webmaster(db=db, webmaster_id=webmaster_id)