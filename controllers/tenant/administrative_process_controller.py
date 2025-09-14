# backend_python/controllers/tenant/administrative_process_controller.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schemas.administrative_process_schema import AdministrativeProcessResponse
from services import administrative_process_service
from middleware.tenant_middleware import get_current_tenant
from middleware.authorize_middleware import has_hierarchical_access

router = APIRouter()

@router.get(
    "/", 
    response_model=List[AdministrativeProcessResponse], 
    summary="Obtém processos administrativos de lojas subordinadas (Exemplo Hierárquico)"
)
async def obter_processos_administrativos(
    db: Session = Depends(get_db),
    current_user: dict = Depends(has_hierarchical_access(['read:administrative_processes'])) # Requer permissão e acesso hierárquico
):
    """Retorna processos administrativos, incluindo os de lojas subordinadas se o usuário tiver acesso hierárquico."""
    # A lógica de filtragem por subordinate_lodge_ids já está no serviço
    # O current_user já contém o tenant e os subordinate_lodge_ids (se aplicável)
    loja_id_atual = current_user["tenant"].id
    subordinate_lodge_ids = current_user.get("subordinate_lodge_ids", [])

    # Inclui a loja do usuário atual na lista de IDs para consulta
    todas_lojas_ids = [loja_id_atual] + subordinate_lodge_ids

    return administrative_process_service.obter_processos_administrativos(
        db=db, 
        subordinate_lodge_ids=todas_lojas_ids
    )
