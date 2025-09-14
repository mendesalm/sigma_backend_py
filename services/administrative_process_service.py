# backend_python/services/administrative_process_service.py

from sqlalchemy.orm import Session
from models.models import ProcessoAdministrativo, Loja
from typing import List, Optional
from fastapi import HTTPException, status

def obter_processos_administrativos(
    db: Session, 
    loja_id: Optional[int] = None, 
    subordinate_lodge_ids: Optional[List[int]] = None
):
    """Retorna processos administrativos, filtrados por loja_id ou IDs de lojas subordinadas."""
    query = db.query(ProcessoAdministrativo)

    if loja_id:
        query = query.filter(ProcessoAdministrativo.loja_id == loja_id)
    elif subordinate_lodge_ids:
        # Inclui a loja do usuário atual na lista de IDs para consulta hierárquica
        # A loja do usuário atual já deve estar no current_user["tenant"].id
        # Esta lógica deve ser passada do controlador, que já terá o current_user
        query = query.filter(ProcessoAdministrativo.loja_id.in_(subordinate_lodge_ids))
    
    return query.all()

def criar_processo_administrativo(db: Session, processo: dict):
    """Cria um novo processo administrativo."""
    # Exemplo básico de criação, adaptar conforme o schema completo
    db_processo = ProcessoAdministrativo(**processo)
    db.add(db_processo)
    db.commit()
    db.refresh(db_processo)
    return db_processo
