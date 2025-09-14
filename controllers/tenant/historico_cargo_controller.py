# backend_python/controllers/tenant/historico_cargo_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.historico_cargo_schema import HistoricoCargoCreate, HistoricoCargoUpdate, HistoricoCargoResponse
from services import historico_cargo_service
from middleware.authorize_middleware import get_current_user

router = APIRouter()

@router.post(
    "/", 
    response_model=HistoricoCargoResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Adiciona um novo registro ao histórico de cargos de um membro"
)
def create_historico_cargo(
    historico: HistoricoCargoCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cria um novo registro de cargo exercido para um membro da loja.
    """
    # Adicionar validação para garantir que o `id_membro` pertence à loja do usuário logado
    return historico_cargo_service.create_historico_cargo(db=db, historico_data=historico)

@router.get(
    "/membro/{membro_id}", 
    response_model=List[HistoricoCargoResponse],
    summary="Lista todo o histórico de cargos de um membro"
)
def get_all_historico_from_membro(
    membro_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna o histórico de cargos de um membro específico.
    """
    # Adicionar validação para garantir que o `membro_id` pertence à loja do usuário logado
    return historico_cargo_service.get_all_historico_from_membro(db=db, membro_id=membro_id)

@router.get(
    "/{historico_id}", 
    response_model=HistoricoCargoResponse, 
    summary="Busca um registro de histórico específico pelo ID"
)
def get_historico(
    historico_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna os detalhes de um registro de histórico de cargo.
    """
    return historico_cargo_service.get_historico_by_id(db=db, historico_id=historico_id)

@router.put(
    "/{historico_id}", 
    response_model=HistoricoCargoResponse, 
    summary="Atualiza um registro de histórico de cargo"
)
def update_historico(
    historico_id: int, 
    historico: HistoricoCargoUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza as informações de um registro de histórico.
    """
    return historico_cargo_service.update_historico_cargo(db=db, historico_id=historico_id, historico_data=historico)

@router.delete(
    "/{historico_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta um registro de histórico de cargo"
)
def delete_historico(
    historico_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Remove um registro de histórico de cargo do sistema.
    """
    historico_cargo_service.delete_historico_cargo(db=db, historico_id=historico_id)
    return
