# backend_python/services/auth_service.py

from sqlalchemy.orm import Session
from models.models import MembroLoja, AssociacaoMembroLoja, Loja, Cargo
from schemas.auth_schema import LodgeMemberLogin, LodgeMemberSelectLodge, LodgeMemberForgotPassword, LodgeMemberResetPassword
from fastapi import HTTPException, status
from datetime import timedelta
import bcrypt
from jose import jwt

from config.settings import config
from utils.auth_utils import criar_token_acesso
from utils.app_errors import AppError

def login_membro_loja(db: Session, dados_login: LodgeMemberLogin):
    """Autentica um membro da loja e retorna um token de acesso."""
    membro = db.query(MembroLoja).filter(MembroLoja.email == dados_login.email).first()

    if not membro or not bcrypt.checkpw(dados_login.senha.encode('utf-8'), membro.senha_hash.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Se o membro pertence a múltiplas associações/cargos, ele precisará selecionar um
    # Por enquanto, pegamos a primeira associação ativa
    associacao = db.query(AssociacaoMembroLoja).filter(
        AssociacaoMembroLoja.lodge_member_id == membro.id
    ).first()

    if not associacao:
        raise AppError("Membro não possui associação ativa com nenhuma loja/cargo.", status.HTTP_401_UNAUTHORIZED)

    # Carrega o cargo e a loja da associação
    db.refresh(associacao, attribute_names=['role', 'lodge_member'])
    db.refresh(associacao.lodge_member, attribute_names=['tenant'])

    if not associacao.role or not associacao.lodge_member.tenant:
        raise AppError("Dados de associação incompletos.", status.HTTP_500_INTERNAL_SERVER_ERROR)

    delta_expiracao = timedelta(minutes=config.MINUTOS_EXPIRACAO_TOKEN_ACESSO)
    token_acesso = criar_token_acesso(
        data={
            "sub": membro.email,
            "perfil": "lodge_member",
            "lodge_member_id": membro.id,
            "association_id": associacao.id,
            "lodge_id": associacao.lodge_member.tenant.id # ID da loja associada
        },
        expires_delta=delta_expiracao
    )
    return {
        "token_de_acesso": token_acesso,
        "tipo_token": "bearer",
        "usuario": {
            "id": membro.id,
            "nome": membro.nome,
            "email": membro.email,
            "cargo": associacao.role.name,
            "loja": associacao.lodge_member.tenant.nome_loja
        }
    }

def selecionar_loja_membro(db: Session, dados_selecao: LodgeMemberSelectLodge, current_user: dict):
    """Permite que um membro da loja selecione uma loja diferente se tiver múltiplas associações."""
    membro_id = current_user["user"].id
    
    # Verifica se o membro tem associação com a loja selecionada
    associacao = db.query(AssociacaoMembroLoja).filter(
        AssociacaoMembroLoja.lodge_member_id == membro_id,
        AssociacaoMembroLoja.lodge_id == dados_selecao.lodge_id # Assumindo que AssociacaoMembroLoja tem lodge_id
    ).first()

    if not associacao:
        raise AppError("Membro não associado a esta loja.", status.HTTP_403_FORBIDDEN)

    # Recria o token com o novo contexto da loja
    db.refresh(associacao, attribute_names=['role', 'lodge_member'])
    db.refresh(associacao.lodge_member, attribute_names=['tenant'])

    delta_expiracao = timedelta(minutes=config.MINUTOS_EXPIRACAO_TOKEN_ACESSO)
    token_acesso = criar_token_acesso(
        data={
            "sub": current_user["user"].email,
            "perfil": "lodge_member",
            "lodge_member_id": membro_id,
            "association_id": associacao.id,
            "lodge_id": associacao.lodge_member.tenant.id
        },
        expires_delta=delta_expiracao
    )
    return {
        "token_de_acesso": token_acesso,
        "tipo_token": "bearer",
        "usuario": {
            "id": membro_id,
            "nome": current_user["user"].nome,
            "email": current_user["user"].email,
            "cargo": associacao.role.name,
            "loja": associacao.lodge_member.tenant.nome_loja
        }
    }

def refresh_token(db: Session, current_user: dict):
    """Gera um novo token de acesso para o usuário atual."""
    # Reutiliza os dados do usuário do token atual para gerar um novo
    perfil = current_user["perfil"]
    sub = current_user["user"].email
    data = {"sub": sub, "perfil": perfil}

    if perfil == "super_admin":
        data["superadmin_id"] = current_user["user"].id
    elif perfil == "webmaster":
        data["webmaster_id"] = current_user["user"].id
    elif perfil == "lodge_member":
        data["lodge_member_id"] = current_user["user"].id
        data["association_id"] = current_user["association"].id
        data["lodge_id"] = current_user["tenant"].id

    delta_expiracao = timedelta(minutes=config.MINUTOS_EXPIRACAO_TOKEN_ACESSO)
    token_acesso = criar_token_acesso(data=data, expires_delta=delta_expiracao)
    
    return {"token_de_acesso": token_acesso, "tipo_token": "bearer"}

def forgot_password(db: Session, dados_esqueci_senha: LodgeMemberForgotPassword):
    """Inicia o processo de recuperação de senha para um membro da loja."""
    membro = db.query(MembroLoja).filter(MembroLoja.email == dados_esqueci_senha.email).first()
    if not membro:
        # Para evitar enumeração de usuários, sempre retorna sucesso
        return {"message": "Se o email estiver registrado, um link de recuperação de senha será enviado."}

    # TODO: Gerar token de recuperação de senha e enviar email
    # Exemplo: token_recuperacao = criar_token_acesso({"sub": membro.email, "tipo": "recuperacao_senha"}, timedelta(hours=1))
    # Enviar email com link para /reset-password?token=token_recuperacao

    return {"message": "Se o email estiver registrado, um link de recuperação de senha será enviado."}


def reset_password(db: Session, dados_reset_senha: LodgeMemberResetPassword):
    """Reseta a senha de um membro da loja usando um token de recuperação."""
    try:
        payload = jwt.decode(dados_reset_senha.token, config.SEGREDO_JWT, algorithms=[config.ALGORITMO])
        email: str = payload.get("sub")
        tipo_token: str = payload.get("tipo")

        if tipo_token != "recuperacao_senha":
            raise AppError("Token inválido para recuperação de senha.", status.HTTP_400_BAD_REQUEST)

    except JWTError:
        raise AppError("Token de recuperação inválido ou expirado.", status.HTTP_401_UNAUTHORIZED)

    membro = db.query(MembroLoja).filter(MembroLoja.email == email).first()
    if not membro:
        raise AppError("Usuário não encontrado.", status.HTTP_404_NOT_FOUND)

    senha_hash = bcrypt.hashpw(dados_reset_senha.nova_senha.encode('utf-8'), bcrypt.gensalt())
    membro.senha_hash = senha_hash.decode('utf-8')
    db.add(membro)
    db.commit()
    db.refresh(membro)

    return {"message": "Senha redefinida com sucesso."}
