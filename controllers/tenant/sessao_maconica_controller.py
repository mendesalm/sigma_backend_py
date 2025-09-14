# backend_python/controllers/tenant/sessao_maconica_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database.connection import get_db
from schemas.sessao_maconica_schema import SessaoMaconicaCreate, SessaoMaconicaUpdate, SessaoMaconicaResponse, SessaoMaconicaUpdateStatus
from services import sessao_maconica_service
from middleware.authorize_middleware import get_current_user

router = APIRouter()

@router.post(
    "/", 
    response_model=SessaoMaconicaResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Cria uma nova sessão maçônica"
)
def create_sessao(
    sessao: SessaoMaconicaCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cria uma nova sessão maçônica para a loja do usuário autenticado.
    """
    # Validação de permissão mais granular pode ser adicionada aqui
    return sessao_maconica_service.create_sessao(db=db, sessao_data=sessao)

@router.get(
    "/", 
    response_model=List[SessaoMaconicaResponse],
    summary="Lista todas as sessões da loja"
)
def get_all_sessoes(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Retorna uma lista de todas as sessões da loja do tenant atual.
    """
    id_loja = current_user['tenant'].id
    return sessao_maconica_service.get_all_sessoes_from_loja(db=db, loja_id=id_loja, skip=skip, limit=limit)

@router.get(
    "/{sessao_id}", 
    response_model=SessaoMaconicaResponse, 
    summary="Busca uma sessão específica pelo ID"
)
def get_sessao(
    sessao_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna os detalhes de uma sessão específica.
    """
    # Adicionar validação para garantir que a sessão pertence à loja do usuário logado
    return sessao_maconica_service.get_sessao_by_id(db=db, sessao_id=sessao_id)

@router.put(
    "/{sessao_id}", 
    response_model=SessaoMaconicaResponse, 
    summary="Atualiza os dados de uma sessão"
)
def update_sessao(
    sessao_id: int, 
    sessao: SessaoMaconicaUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza as informações de uma sessão existente.
    """
    # Adicionar validação para garantir que a sessão pertence à loja do usuário logado
    return sessao_maconica_service.update_sessao(db=db, sessao_id=sessao_id, sessao_data=sessao)

@router.delete(
    "/{sessao_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta uma sessão"
)
def delete_sessao(
    sessao_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Remove uma sessão do sistema.
    """
    # Adicionar validação para garantir que a sessão pertence à loja do usuário logado
    sessao_maconica_service.delete_sessao(db=db, sessao_id=sessao_id)
    return

@router.put(
    "/{sessao_id}/status", 
    response_model=SessaoMaconicaResponse, 
    summary="Atualiza o status de uma sessão"
)
def update_sessao_status(
    sessao_id: int, 
    status_update: SessaoMaconicaUpdateStatus, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza o status de uma sessão específica (Agendada, Em Andamento, Realizada, Cancelada).
    """
    # Adicionar validação para garantir que a sessão pertence à loja do usuário logado
    return sessao_maconica_service.update_sessao_status(db=db, sessao_id=sessao_id, new_status=status_update.status)

@router.get(
    "/sugerir-proxima", 
    response_model=Optional[datetime], 
    summary="Sugere a próxima data e hora de sessão para a loja"
)
def suggest_next_session_date(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Sugere a próxima data e hora de sessão para a loja do tenant atual, com base na periodicidade configurada.
    Retorna null se não for possível fazer a sugestão.
    """
    id_loja = current_user['tenant'].id
    return sessao_maconica_service.suggest_next_session_date(db=db, loja_id=id_loja)
