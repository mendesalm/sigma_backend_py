# backend_python/services/role_service.py

from sqlalchemy.orm import Session
from models.models import Cargo, ClasseLoja
from schemas.role_schema import RoleCreate, RoleUpdate
from fastapi import HTTPException, status

def criar_cargo(db: Session, cargo: RoleCreate):
    """Cria um novo cargo no banco de dados."""
    if cargo.lodge_class_id:
        classe_loja = db.query(ClasseLoja).filter(ClasseLoja.id == cargo.lodge_class_id).first()
        if not classe_loja:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classe de Loja não encontrada.")

    db_cargo = Cargo(name=cargo.name, lodge_class_id=cargo.lodge_class_id)
    db.add(db_cargo)
    db.commit()
    db.refresh(db_cargo)
    return db_cargo

def obter_todos_cargos(db: Session):
    """Retorna todos os cargos do banco de dados."""
    return db.query(Cargo).all()

def obter_cargo_por_id(db: Session, cargo_id: int):
    """Retorna um cargo específico pelo ID."""
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not cargo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cargo não encontrado.")
    return cargo

def atualizar_cargo(db: Session, cargo_id: int, cargo_atualizacao: RoleUpdate):
    """Atualiza um cargo existente no banco de dados."""
    db_cargo = obter_cargo_por_id(db, cargo_id)
    
    if cargo_atualizacao.lodge_class_id:
        classe_loja = db.query(ClasseLoja).filter(ClasseLoja.id == cargo_atualizacao.lodge_class_id).first()
        if not classe_loja:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classe de Loja não encontrada.")

    update_data = cargo_atualizacao.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cargo, key, value)

    db.add(db_cargo)
    db.commit()
    db.refresh(db_cargo)
    return db_cargo

def deletar_cargo(db: Session, cargo_id: int):
    """Deleta um cargo do banco de dados."""
    db_cargo = obter_cargo_por_id(db, cargo_id)
    db.delete(db_cargo)
    db.commit()
    return {"mensagem": "Cargo deletado com sucesso."}
