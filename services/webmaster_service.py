# backend_python/services/webmaster_service.py

from sqlalchemy.orm import Session
from models.models import Webmaster
from schemas.webmaster_schema import WebmasterUpdateEmail
from utils.password_utils import generate_secure_password
from fastapi import HTTPException, status
import bcrypt

def obter_webmaster_por_id(db: Session, webmaster_id: int):
    """Retorna um webmaster específico pelo ID."""
    webmaster = db.query(Webmaster).filter(Webmaster.id == webmaster_id).first()
    if not webmaster:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webmaster não encontrado.")
    return webmaster

def resetar_senha_webmaster(db: Session, webmaster_id: int):
    """Reseta a senha de um webmaster e retorna a nova senha gerada."""
    db_webmaster = obter_webmaster_por_id(db, webmaster_id)

    nova_senha = generate_secure_password()
    senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())

    db_webmaster.senha_hash = senha_hash.decode('utf-8')
    db.add(db_webmaster)
    db.commit()
    db.refresh(db_webmaster)

    return {"message": "Senha do webmaster resetada com sucesso.", "new_password": nova_senha}

def atualizar_email_webmaster(db: Session, webmaster_id: int, email_atualizacao: WebmasterUpdateEmail):
    """Atualiza o email de um webmaster existente."""
    db_webmaster = obter_webmaster_por_id(db, webmaster_id)

    db_webmaster.email = email_atualizacao.email
    db.add(db_webmaster)
    db.commit()
    db.refresh(db_webmaster)
    return db_webmaster
