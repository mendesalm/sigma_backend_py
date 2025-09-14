# backend_python/utils/auth_utils.py

from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Optional

from config.settings import config

def criar_token_acesso(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um novo token de acesso JWT."""
    a_codificar = data.copy()
    if expires_delta:
        expira_em = datetime.now(timezone.utc) + expires_delta
    else:
        expira_em = datetime.now(timezone.utc) + timedelta(minutes=15)
    a_codificar.update({"exp": expira_em})
    token_jwt_codificado = jwt.encode(a_codificar, config.SEGREDO_JWT, algorithm=config.ALGORITMO)
    return token_jwt_codificado
