# backend_python/middleware/authorize_middleware.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config.settings import config
from database.connection import get_db
from models.models import SuperAdministrador, Webmaster, MembroLoja

# Define o esquema de autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/global/superadmins/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Decodifica o token JWT para obter o usuário atual.
    Esta função é uma dependência que pode ser usada em qualquer endpoint protegido.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # CORRIGIDO: Usa o algoritmo "HS256" diretamente
        payload = jwt.decode(token, config.SEGREDO_JWT, algorithms=["HS256"])
        perfil: str = payload.get("perfil")
        if perfil is None:
            raise credentials_exception

        user_data = {"perfil": perfil}
        if perfil == "super_admin":
            user_id = payload.get("superadmin_id")
            user = db.query(SuperAdministrador).filter(SuperAdministrador.id == user_id).first()
        elif perfil == "webmaster":
            user_id = payload.get("webmaster_id")
            user = db.query(Webmaster).filter(Webmaster.id == user_id).first()
        elif perfil == "lodge_member":
            user_id = payload.get("lodgeMemberId")
            user = db.query(MembroLoja).filter(MembroLoja.id == user_id).first()
        else:
            raise credentials_exception

        if user is None:
            raise credentials_exception
        
        user_data["user"] = user
        return user_data

    except JWTError:
        raise credentials_exception