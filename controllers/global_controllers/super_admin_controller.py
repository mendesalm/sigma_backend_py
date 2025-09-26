# backend_python/controllers/global/super_admin_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt
from datetime import timedelta
from typing import List

from database.connection import get_db
from models.models import SuperAdministrador
from schemas.super_admin_schema import SuperAdminCreate, SuperAdminLogin, SuperAdminUpdate, SuperAdminResponse
from config.settings import config
from utils.auth_utils import criar_token_acesso
from middleware.authorize_middleware import get_current_user

router = APIRouter()

# Dependência para garantir que o usuário é um SuperAdmin
async def get_current_super_admin(current_user_data: dict = Depends(get_current_user)) -> SuperAdministrador:
    if current_user_data.get("perfil") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas Super Administradores podem realizar esta ação."
        )
    return current_user_data.get("user")

@router.post(
    "/login", 
    response_model=dict, 
    summary="Autentica um super administrador e retorna um token de acesso"
)
async def login_super_admin(
    dados_login: SuperAdminLogin, 
    db: Session = Depends(get_db)
):
    """Autentica um super administrador e retorna um token de acesso JWT.""" 
    super_admin = db.query(SuperAdministrador).filter(SuperAdministrador.email == dados_login.email).first()

    if not super_admin or not bcrypt.checkpw(dados_login.password.encode('utf-8'), super_admin.senha_hash.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # CORRIGIDO: Usa a variável de configuração correta (EXPIRACAO_JWT)
    exp_hours = int(config.EXPIRACAO_JWT.replace('h', ''))
    delta_expiracao = timedelta(hours=exp_hours)
    
    token_data = {
        "perfil": "super_admin",
        "superadmin_id": super_admin.id
    }
    token_acesso = criar_token_acesso(
        data=token_data,
        expires_delta=delta_expiracao
    )
    return {"token_de_acesso": token_acesso, "tipo_token": "bearer"}

@router.post(
    "/",
    response_model=SuperAdminResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo super administrador (Requer autenticação de SuperAdmin)"
)
async def criar_super_admin(
    dados_registro: SuperAdminCreate,
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Cria um novo super administrador."""
    if db.query(SuperAdministrador).filter(SuperAdministrador.email == dados_registro.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Um super administrador com este email já existe."
        )

    senha_hash = bcrypt.hashpw(dados_registro.password.encode('utf-8'), bcrypt.gensalt())

    novo_super_admin = SuperAdministrador(
        nome_usuario=dados_registro.nome_usuario,
        email=dados_registro.email,
        senha_hash=senha_hash.decode('utf-8')
    )

    db.add(novo_super_admin)
    db.commit()
    db.refresh(novo_super_admin)

    return novo_super_admin

@router.post(
    "/initial_register", 
    response_model=SuperAdminResponse, 
    summary="Registra o primeiro super administrador (apenas se nenhum existir)"
)
async def registrar_super_admin_inicial(
    dados_registro: SuperAdminCreate, 
    db: Session = Depends(get_db)
):
    """
    Registra o primeiro super administrador do sistema.
    Este endpoint só funciona se nenhum outro super administrador existir.
    """
    if db.query(SuperAdministrador).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Um super administrador já existe. Não é possível registrar outro."
        )

    senha_hash = bcrypt.hashpw(dados_registro.password.encode('utf-8'), bcrypt.gensalt())

    novo_super_admin = SuperAdministrador(
        nome_usuario=dados_registro.nome_usuario,
        email=dados_registro.email,
        senha_hash=senha_hash.decode('utf-8'),
        is_root=True # Marca o primeiro como root
    )

    db.add(novo_super_admin)
    db.commit()
    db.refresh(novo_super_admin)

    return novo_super_admin

@router.get(
    "/", 
    response_model=List[SuperAdminResponse], 
    summary="Lista todos os super administradores (Requer autenticação de SuperAdmin)"
)
async def listar_super_administradores(
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Retorna uma lista de todos os super administradores."""
    super_administradores = db.query(SuperAdministrador).all()
    return super_administradores

@router.get(
    "/{super_admin_id}", 
    response_model=SuperAdminResponse, 
    summary="Obtém um super administrador pelo ID (Requer autenticação de SuperAdmin)"
)
async def obter_super_admin_por_id(
    super_admin_id: int, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Retorna um super administrador específico pelo seu ID."""
    super_admin = db.query(SuperAdministrador).filter(SuperAdministrador.id == super_admin_id).first()
    if not super_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Super Administrador não encontrado.")
    return super_admin

@router.put(
    "/{super_admin_id}", 
    response_model=SuperAdminResponse, 
    summary="Atualiza um super administrador (Requer autenticação de SuperAdmin)"
)
async def atualizar_super_admin(
    super_admin_id: int, 
    dados_atualizacao: SuperAdminUpdate, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Atualiza as informações de um super administrador existente."""
    super_admin = db.query(SuperAdministrador).filter(SuperAdministrador.id == super_admin_id).first()
    if not super_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Super Administrador não encontrado.")

    # Impede a desativação do admin root
    if super_admin.is_root and dados_atualizacao.esta_ativo is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="O SuperAdmin principal não pode ser desativado.")

    update_data = dados_atualizacao.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["senha_hash"] = bcrypt.hashpw(update_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        del update_data["password"]
    
    for key, value in update_data.items():
        setattr(super_admin, key, value)

    db.add(super_admin)
    db.commit()
    db.refresh(super_admin)
    return super_admin

@router.delete(
    "/{super_admin_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Deleta um super administrador (Requer autenticação de SuperAdmin)"
)
async def deletar_super_admin(
    super_admin_id: int, 
    db: Session = Depends(get_db),
    current_admin: SuperAdministrador = Depends(get_current_super_admin)
):
    """Deleta um super administrador pelo ID."""
    super_admin = db.query(SuperAdministrador).filter(SuperAdministrador.id == super_admin_id).first()
    if not super_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Super Administrador não encontrado.")

    if super_admin.is_root:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="O SuperAdmin principal não pode ser excluído.")
    
    db.delete(super_admin)
    db.commit()
    return None
