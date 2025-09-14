# backend_python/middleware/tenant_middleware.py

from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import Session
from models.models import Loja
from database.connection import get_db

async def get_current_tenant(
    x_lodge_code: str = Header(..., alias="x-lodge-code"),
    db: Session = Depends(get_db)
) -> Loja:
    """
    Dependência FastAPI para identificar o tenant a partir do cabeçalho 'x-lodge-code'.
    Retorna o objeto Loja correspondente ou levanta uma exceção HTTP.
    """
    if not x_lodge_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cabeçalho 'x-lodge-code' é obrigatório."
        )

    tenant = db.query(Loja).filter(
        Loja.codigo_loja == x_lodge_code,
        Loja.esta_ativo == True
    ).first()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant não encontrado ou inativo."
        )
    
    return tenant
