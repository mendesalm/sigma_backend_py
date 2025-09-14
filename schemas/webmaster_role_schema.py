# backend_python/schemas/webmaster_role_schema.py

from pydantic import BaseModel, Field
from typing import Optional

class WebmasterRoleAssignment(BaseModel):
    lodge_member_association_id: int = Field(..., description="ID da associação do membro da loja.")
    role_id: Optional[int] = Field(None, description="ID do cargo a ser atribuído (nulo para remover)." )

class WebmasterRoleResponse(BaseModel):
    lodge_member_association_id: int
    role_id: Optional[int]
    role_name: Optional[str] = None

