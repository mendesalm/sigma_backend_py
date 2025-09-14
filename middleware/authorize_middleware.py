# backend_python/middleware/authorize_middleware.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import List, Optional

from config.settings import config
from database.connection import get_db
from models.models import SuperAdministrador, Webmaster, Loja, MembroLoja, Cargo, Permissao, AssociacaoMembroLoja, HierarquiaLoja
from utils.app_errors import AppError

# Esquema de autenticação OAuth2 para o token Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/super_administradores/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Decodifica o token JWT, identifica o tipo de usuário e retorna o objeto do usuário
    com seu perfil, cargo e tenant associados.
    """
    try:
        payload = jwt.decode(token, config.SEGREDO_JWT, algorithms=[config.ALGORITMO])
        perfil_usuario: str = payload.get("perfil")

        if perfil_usuario == "super_admin":
            superadmin_id: int = payload.get("superadmin_id")
            superadmin = db.query(SuperAdministrador).filter(SuperAdministrador.id == superadmin_id).first()
            if not superadmin:
                raise AppError("SuperAdmin pertencente a este token não existe mais.", status.HTTP_401_UNAUTHORIZED)
            return {"user": superadmin, "perfil": "super_admin", "role": {"name": "SuperAdmin"}, "tenant": None}

        elif perfil_usuario == "webmaster":
            webmaster_id: int = payload.get("webmaster_id")
            webmaster = db.query(Webmaster).filter(Webmaster.id == webmaster_id).first()
            if not webmaster:
                raise AppError("Webmaster pertencente a este token não existe mais.", status.HTTP_401_UNAUTHORIZED)
            # Webmaster tem acesso irrestrito dentro do seu tenant
            tenant = db.query(Loja).filter(Loja.id == webmaster.id_loja).first()
            if not tenant:
                raise AppError("Tenant do Webmaster não encontrado.", status.HTTP_401_UNAUTHORIZED)
            return {"user": webmaster, "perfil": "webmaster", "role": {"name": "Webmaster"}, "tenant": tenant}

        elif perfil_usuario == "lodge_member":
            lodge_member_id: int = payload.get("lodge_member_id")
            association_id: int = payload.get("association_id")
            
            associacao = db.query(AssociacaoMembroLoja).filter(
                AssociacaoMembroLoja.id == association_id,
                AssociacaoMembroLoja.lodge_member_id == lodge_member_id
            ).first()

            if not associacao:
                raise AppError("Associação de membro da loja não encontrada ou inválida.", status.HTTP_401_UNAUTHORIZED)
            
            # Carrega os relacionamentos
            db.refresh(associacao, attribute_names=['role', 'lodge_member'])
            db.refresh(associacao.role, attribute_names=['permissoes_associadas'])
            db.refresh(associacao.lodge_member, attribute_names=['tenant'])

            if not associacao.role or not associacao.lodge_member or not associacao.lodge_member.tenant:
                 raise AppError("Dados de associação incompletos.", status.HTTP_401_UNAUTHORIZED)

            # Mapeia as permissões para o formato esperado
            permissoes_do_cargo = [p.permission for p in associacao.role.permissoes_associadas]
            
            return {
                "user": associacao.lodge_member,
                "perfil": "lodge_member",
                "role": {"name": associacao.role.name, "permissions": permissoes_do_cargo},
                "tenant": associacao.lodge_member.tenant,
                "association": associacao
            }

        else:
            raise AppError("Perfil de usuário inválido no token.", status.HTTP_401_UNAUTHORIZED)

    except JWTError:
        raise AppError("Token inválido ou expirado.", status.HTTP_401_UNAUTHORIZED)

def has_permission(required_permissions: List[str]):
    """
    Dependência que verifica se o usuário atual tem as permissões necessárias.
    SuperAdmins e Webmasters têm acesso irrestrito.
    """
    async def _check_permission(current_user: dict = Depends(get_current_user)):
        perfil = current_user.get("perfil")
        
        # SuperAdmin e Webmaster têm acesso irrestrito
        if perfil in ["super_admin", "webmaster"]:
            return current_user

        # Para LodgeMembers, verifica as permissões
        if perfil == "lodge_member":
            user_permissions = [p.action for p in current_user["role"]["permissions"]]
            if not all(rp in user_permissions for rp in required_permissions):
                raise AppError("Você não tem permissão para realizar esta ação.", status.HTTP_403_FORBIDDEN)
            return current_user
        
        raise AppError("Acesso não autorizado.", status.HTTP_401_UNAUTHORIZED)

    return _check_permission

def has_hierarchical_access(required_permissions: List[str]):
    """
    Dependência que verifica permissões e, para cargos hierárquicos, anexa IDs de lojas subordinadas.
    """
    async def _check_hierarchical_access(current_user: dict = Depends(has_permission(required_permissions))):
        perfil = current_user.get("perfil")

        # SuperAdmin e Webmaster já têm acesso irrestrito, não precisam de lógica hierárquica adicional aqui
        if perfil in ["super_admin", "webmaster"]:
            return current_user

        # Apenas LodgeMembers de cargos com hierarquia (ex: Grão-Mestre) precisam desta lógica
        if perfil == "lodge_member":
            tenant = current_user.get("tenant")
            role = current_user.get("role")

            # Verifica se o cargo tem a capacidade de ter subordinados (ex: Grão-Mestre)
            # Isso pode ser um atributo no modelo Cargo ou uma verificação de nome de cargo
            # Por simplicidade, vamos assumir que certos nomes de cargo implicam hierarquia
            if role and role["name"] in ["Grão-Mestre", "Venerável Mestre"]: # Exemplo: ajustar conforme a regra de negócio
                # Busca lojas subordinadas
                subordinate_lodges = db.query(HierarquiaLoja).filter(
                    HierarquiaLoja.superior_lodge_id == tenant.id
                ).all()
                current_user["subordinate_lodge_ids"] = [lh.subordinate_lodge_id for lh in subordinate_lodges]
            else:
                current_user["subordinate_lodge_ids"] = [] # Nenhuma loja subordinada para este perfil/cargo

            return current_user
        
        raise AppError("Acesso hierárquico não autorizado.", status.HTTP_401_UNAUTHORIZED)

    return _check_hierarchical_access
