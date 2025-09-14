# backend_python/services/membro_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import bcrypt

from models.models import MembroLoja, Loja
from schemas.membro_schema import MembroCreate, MembroUpdate

def create_membro(db: Session, membro_data: MembroCreate) -> MembroLoja:
    """Cria um novo membro no banco de dados."""
    # Valida se a loja existe
    loja = db.query(Loja).filter(Loja.id == membro_data.id_loja).first()
    if not loja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Loja com id {membro_data.id_loja} não encontrada.")

    # Valida se o email já está em uso
    db_membro = db.query(MembroLoja).filter(MembroLoja.email == membro_data.email).first()
    if db_membro:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado.")

    # Criptografa a senha
    senha_hash = bcrypt.hashpw(membro_data.senha.encode('utf-8'), bcrypt.gensalt())

    # Cria o objeto do novo membro
    novo_membro = MembroLoja(
        **membro_data.model_dump(exclude={'senha'}),
        senha_hash=senha_hash.decode('utf-8')
    )

    db.add(novo_membro)
    db.commit()
    db.refresh(novo_membro)
    return novo_membro

def get_membro_by_id(db: Session, membro_id: int) -> MembroLoja:
    """Busca um membro pelo seu ID."""
    membro = db.query(MembroLoja).filter(MembroLoja.id == membro_id).first()
    if not membro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membro não encontrado.")
    return membro

def get_all_membros_from_loja(db: Session, loja_id: int, skip: int = 0, limit: int = 100):
    """Lista todos os membros de uma loja específica."""
    return db.query(MembroLoja).filter(MembroLoja.id_loja == loja_id).offset(skip).limit(limit).all()

def update_membro(db: Session, membro_id: int, membro_data: MembroUpdate) -> MembroLoja:
    """Atualiza os dados de um membro."""
    db_membro = get_membro_by_id(db, membro_id)

    update_data = membro_data.model_dump(exclude_unset=True)

    # Se a senha for fornecida, criptografa a nova senha
    if "senha" in update_data and update_data["senha"]:
        senha_hash = bcrypt.hashpw(update_data["senha"].encode('utf-8'), bcrypt.gensalt())
        db_membro.senha_hash = senha_hash.decode('utf-8')
        del update_data["senha"]

    for key, value in update_data.items():
        setattr(db_membro, key, value)

    db.commit()
    db.refresh(db_membro)
    return db_membro

def delete_membro(db: Session, membro_id: int):
    """Deleta um membro do banco de dados."""
    db_membro = get_membro_by_id(db, membro_id)
    db.delete(db_membro)
    db.commit()
    return {"ok": True}
