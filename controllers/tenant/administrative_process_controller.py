# backend_python/controllers/tenant/administrative_process_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.administrative_process_schema import AdministrativeProcessCreate, AdministrativeProcessUpdate, AdministrativeProcessResponse
from services import administrative_process_service
# A função 'has_hierarchical_access' não está implementada, então a importação e uso foram comentados.
from middleware.authorize_middleware import get_current_user #, has_hierarchical_access

router = APIRouter()

@router.post("/", response_model=AdministrativeProcessResponse, status_code=status.HTTP_201_CREATED)
def create_administrative_process(
    process: AdministrativeProcessCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    return administrative_process_service.create_process(db=db, process=process, user_id=current_user["user"].id)

@router.get("/", response_model=List[AdministrativeProcessResponse])
def get_all_administrative_processes(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    return administrative_process_service.get_all_processes(db=db, user_id=current_user["user"].id)

@router.get("/{process_id}", response_model=AdministrativeProcessResponse)
def get_administrative_process(
    process_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Proteção básica adicionada
    # has_access: bool = Depends(has_hierarchical_access) # TODO: Implementar lógica de acesso hierárquico
):
    # Por enquanto, qualquer usuário autenticado no tenant pode acessar.
    return administrative_process_service.get_process(db=db, process_id=process_id)

@router.put("/{process_id}", response_model=AdministrativeProcessResponse)
def update_administrative_process(
    process_id: int, 
    process_update: AdministrativeProcessUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Proteção básica adicionada
    # has_access: bool = Depends(has_hierarchical_access) # TODO: Implementar lógica de acesso hierárquico
):
    return administrative_process_service.update_process(db=db, process_id=process_id, process_update=process_update)

@router.delete("/{process_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_administrative_process(
    process_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Proteção básica adicionada
    # has_access: bool = Depends(has_hierarchical_access) # TODO: Implementar lógica de acesso hierárquico
):
    administrative_process_service.delete_process(db=db, process_id=process_id)
    return