# backend_python/controllers/tenant/familiar_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.familiar_schema import FamiliarCreate, FamiliarUpdate, FamiliarResponse
from services import familiar_service
from middleware.authorize_middleware import get_current_user

router = APIRouter()

@router.post(
    "/", 
    response_model=FamiliarResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Adiciona um novo familiar a um membro"
)
def create_familiar(
    familiar: FamiliarCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cria um novo registro de familiar para um membro da loja.
    """
    # Adicionar validação para garantir que o `id_membro` pertence à loja do usuário logado
    return familiar_service.create_familiar(db=db, familiar_data=familiar)

@router.get(
    "/membro/{membro_id}", 
    response_model=List[FamiliarResponse],
    summary="Lista todos os familiares de um membro"
)
def get_all_familiares_from_membro(
    membro_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna uma lista de todos os familiares de um membro específico.
    """
    # Adicionar validação para garantir que o `membro_id` pertence à loja do usuário logado
    return familiar_service.get_all_familiares_from_membro(db=db, membro_id=membro_id)

@router.get(
    "/{familiar_id}", 
    response_model=FamiliarResponse, 
    summary="Busca um familiar específico pelo ID"
)
def get_familiar(
    familiar_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna os detalhes de um familiar específico.
    """
    return familiar_service.get_familiar_by_id(db=db, familiar_id=familiar_id)

@router.put(
    "/{familiar_id}", 
    response_model=FamiliarResponse, 
    summary="Atualiza os dados de um familiar"
)
def update_familiar(
    familiar_id: int, 
    familiar: FamiliarUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza as informações de um familiar existente.
    """
    return familiar_service.update_familiar(db=db, familiar_id=familiar_id, familiar_data=familiar)

@router.delete(
    "/{familiar_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta um familiar"
)
def delete_familiar(
    familiar_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Remove um familiar do sistema.
    """
    familiar_service.delete_familiar(db=db, familiar_id=familiar_id)
    return
