# backend_python/controllers/global/webmaster_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.webmaster_schema import WebmasterUpdateEmail, WebmasterResetPasswordResponse
from services import webmaster_service

router = APIRouter()

@router.put(
    "/{webmaster_id}/reset-password", 
    response_model=WebmasterResetPasswordResponse, 
    summary="Reseta a senha de um webmaster"
)
async def resetar_senha_webmaster(
    webmaster_id: int, 
    db: Session = Depends(get_db)
):
    """Reseta a senha de um webmaster específico e retorna a nova senha gerada."""
    return webmaster_service.resetar_senha_webmaster(db=db, webmaster_id=webmaster_id)

@router.put(
    "/{webmaster_id}/email", 
    response_model=WebmasterUpdateEmail, 
    summary="Atualiza o email de um webmaster"
)
async def atualizar_email_webmaster(
    webmaster_id: int, 
    email_atualizacao: WebmasterUpdateEmail, 
    db: Session = Depends(get_db)
):
    """Atualiza o email de um webmaster específico."""
    return webmaster_service.atualizar_email_webmaster(db=db, webmaster_id=webmaster_id, email_atualizacao=email_atualizacao)
