# backend_python/controllers/tenant/presenca_sessao_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.presenca_sessao_schema import PresencaSessaoCreate, PresencaSessaoResponse
from services import presenca_sessao_service
from middleware.authorize_middleware import get_current_user

router = APIRouter()

@router.post(
    "/", 
    response_model=PresencaSessaoResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Registra uma nova presença em sessão (manual)"
)
def create_presenca(
    presenca: PresencaSessaoCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Registra manualmente a presença de um membro ou visitante em uma sessão.
    Requer permissão específica (ex: Chanceler).
    """
    # TODO: Adicionar verificação de permissão específica (e.g., sessao:gerenciar_presenca)
    return presenca_sessao_service.create_presenca(db=db, presenca_data=presenca)

@router.get(
    "/sessao/{sessao_id}", 
    response_model=List[PresencaSessaoResponse],
    summary="Lista todas as presenças de uma sessão específica"
)
def get_all_presencas_from_sessao(
    sessao_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna uma lista de todos os registros de presença para uma sessão específica.
    """
    # TODO: Adicionar verificação de permissão e que a sessão pertence à loja do usuário logado
    return presenca_sessao_service.get_all_presencas_from_sessao(db=db, sessao_id=sessao_id)

@router.get(
    "/{presenca_id}", 
    response_model=PresencaSessaoResponse, 
    summary="Busca um registro de presença específico pelo ID"
)
def get_presenca(
    presenca_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna os detalhes de um registro de presença específico.
    """
    # TODO: Adicionar verificação de permissão e que a presença pertence à loja do usuário logado
    return presenca_sessao_service.get_presenca_by_id(db=db, presenca_id=presenca_id)

@router.delete(
    "/{presenca_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta um registro de presença"
)
def delete_presenca(
    presenca_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Remove um registro de presença do sistema.
    """
    # TODO: Adicionar verificação de permissão e que a presença pertence à loja do usuário logado
    presenca_sessao_service.delete_presenca(db=db, presenca_id=presenca_id)
    return

@router.post(
    "/checkin", 
    response_model=PresencaSessaoResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Realiza o check-in de presença via QR Code"
)
def checkin_via_qr_code(
    sessao_id: int, # ID da sessão obtido do QR Code
    id_loja_qr_code: int, # ID da loja obtido do QR Code
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Usuário autenticado via app
):
    """
    Endpoint para o check-in de presença via leitura de QR Code por aplicativo móvel.
    Valida a janela de tempo e registra a presença.
    """
    return presenca_sessao_service.checkin_presenca(db=db, sessao_id=sessao_id, id_loja_qr_code=id_loja_qr_code, current_user=current_user)
