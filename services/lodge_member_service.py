# backend_python/services/lodge_member_service.py

from sqlalchemy.orm import Session
from models.models import MembroLoja, AssociacaoMembroLoja, Cargo, Loja
from schemas.lodge_member_schema import LodgeMemberCreate, LodgeMemberUpdate
from fastapi import HTTPException, status
import bcrypt

def criar_membro_loja(db: Session, membro: LodgeMemberCreate, tenant_id: int):
    """Cria um novo membro da loja e sua associação com um cargo."""
    # Verifica se o tenant existe
    loja = db.query(Loja).filter(Loja.id == tenant_id).first()
    if not loja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada.")

    # Verifica se o cargo existe
    cargo = db.query(Cargo).filter(Cargo.id == membro.role_id).first()
    if not cargo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cargo não encontrado.")

    # Cria o MembroLoja
    senha_hash = bcrypt.hashpw(membro.senha.encode('utf-8'), bcrypt.gensalt())
    novo_membro = MembroLoja(
        nome=membro.nome,
        email=membro.email,
        senha_hash=senha_hash.decode('utf-8'),
        tenant_id=tenant_id
    )
    db.add(novo_membro)
    db.commit()
    db.refresh(novo_membro)

    # Cria a AssociaçãoMembroLoja
    nova_associacao = AssociacaoMembroLoja(
        lodge_member_id=novo_membro.id,
        role_id=membro.role_id
    )
    db.add(nova_associacao)
    db.commit()
    db.refresh(nova_associacao)

    return novo_membro

def obter_todos_membros_loja(db: Session, tenant_id: int):
    """Retorna todos os membros de uma loja específica."""
    return db.query(MembroLoja).filter(MembroLoja.tenant_id == tenant_id).all()

def obter_membro_loja_por_id(db: Session, membro_id: int, tenant_id: int):
    """Retorna um membro da loja específico pelo ID e tenant_id."""
    membro = db.query(MembroLoja).filter(
        MembroLoja.id == membro_id,
        MembroLoja.tenant_id == tenant_id
    ).first()
    if not membro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membro da Loja não encontrado.")
    return membro

def atualizar_membro_loja(db: Session, membro_id: int, tenant_id: int, membro_atualizacao: LodgeMemberUpdate):
    """Atualiza as informações de um membro da loja existente."""
    db_membro = obter_membro_loja_por_id(db, membro_id, tenant_id)
    
    update_data = membro_atualizacao.model_dump(exclude_unset=True)
    
    if "senha" in update_data and update_data["senha"]:
        update_data["senha_hash"] = bcrypt.hashpw(update_data["senha"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        del update_data["senha"]
    
    if "role_id" in update_data and update_data["role_id"]:
        # Atualiza a associação de cargo
        cargo = db.query(Cargo).filter(Cargo.id == update_data["role_id"]).first()
        if not cargo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Novo Cargo não encontrado.")
        
        associacao = db.query(AssociacaoMembroLoja).filter(
            AssociacaoMembroLoja.lodge_member_id == membro_id
        ).first()
        if associacao:
            associacao.role_id = update_data["role_id"]
            db.add(associacao)
        else:
            # Cria nova associação se não existir (caso improvável)
            nova_associacao = AssociacaoMembroLoja(lodge_member_id=membro_id, role_id=update_data["role_id"])
            db.add(nova_associacao)
        del update_data["role_id"]

    for key, value in update_data.items():
        if key != "senha": # Senha já tratada
            setattr(db_membro, key, value)

    db.add(db_membro)
    db.commit()
    db.refresh(db_membro)
    return db_membro

def deletar_membro_loja(db: Session, membro_id: int, tenant_id: int):
    """Deleta um membro da loja e suas associações."""
    db_membro = obter_membro_loja_por_id(db, membro_id, tenant_id)
    
    # Deleta associações primeiro
    db.query(AssociacaoMembroLoja).filter(AssociacaoMembroLoja.lodge_member_id == membro_id).delete()
    
    db.delete(db_membro)
    db.commit()
    return {"mensagem": "Membro da Loja deletado com sucesso."}
