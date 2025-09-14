# backend_python/controllers/tenant/condecoracao_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.condecoracao_schema import CondecoracaoCreate, CondecoracaoUpdate, CondecoracaoResponse
from services import condecoracao_service
from middleware.authorize_middleware import get_current_user

router = APIRouter()

@router.post(
    "/", 
    response_model=CondecoracaoResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Adiciona uma nova condecoração a um membro"
)
def create_condecoracao(
    condecoracao: CondecoracaoCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cria um novo registro de condecoração para um membro da loja.
    """
    # Adicionar validação para garantir que o `id_membro` pertence à loja do usuário logado
    return condecoracao_service.create_condecoracao(db=db, condecoracao_data=condecoracao)

@router.get(
    "/membro/{membro_id}", 
    response_model=List[CondecoracaoResponse],
    summary="Lista todas as condecorações de um membro"
)
def get_all_condecoracoes_from_membro(
    membro_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna uma lista de todas as condecorações de um membro específico.
    """
    # Adicionar validação para garantir que o `membro_id` pertence à loja do usuário logado
    return condecoracao_service.get_all_condecoracoes_from_membro(db=db, membro_id=membro_id)

@router.get(
    "/{condecoracao_id}", 
    response_model=CondecoracaoResponse, 
    summary="Busca uma condecoração específica pelo ID"
)
def get_condecoracao(
    condecoracao_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna os detalhes de uma condecoração específica.
    """
    return condecoracao_service.get_condecoracao_by_id(db=db, condecoracao_id=condecoracao_id)

@router.put(
    "/{condecoracao_id}", 
    response_model=CondecoracaoResponse, 
    summary="Atualiza os dados de uma condecoração"
)
def update_condecoracao(
    condecoracao_id: int, 
    condecoracao: CondecoracaoUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza as informações de uma condecoração existente.
    """
    return condecoracao_service.update_condecoracao(db=db, condecoracao_id=condecoracao_id, condecoracao_data=condecoracao)

@router.delete(
    "/{condecoracao_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta uma condecoração"
)
def delete_condecoracao(
    condecoracao_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Remove uma condecoração do sistema.
    """
    condecoracao_service.delete_condecoracao(db=db, condecoracao_id=condecoracao_id)
    return
