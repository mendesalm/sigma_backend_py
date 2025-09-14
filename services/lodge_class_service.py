# backend_python/services/lodge_class_service.py

from sqlalchemy.orm import Session
from models.models import ClasseLoja
from schemas.lodge_class_schema import LodgeClassCreate, LodgeClassUpdate
from fastapi import HTTPException, status

def criar_classe_loja(db: Session, classe_loja: LodgeClassCreate):
    """Cria uma nova classe de loja no banco de dados."""
    db_classe_loja = ClasseLoja(nome=classe_loja.nome, descricao=classe_loja.descricao)
    db.add(db_classe_loja)
    db.commit()
    db.refresh(db_classe_loja)
    return db_classe_loja

def obter_todas_classes_loja(db: Session):
    """Retorna todas as classes de loja do banco de dados."""
    return db.query(ClasseLoja).all()

def obter_classe_loja_por_id(db: Session, classe_loja_id: int):
    """Retorna uma classe de loja específica pelo ID."""
    classe_loja = db.query(ClasseLoja).filter(ClasseLoja.id == classe_loja_id).first()
    if not classe_loja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classe de Loja não encontrada.")
    return classe_loja

def atualizar_classe_loja(db: Session, classe_loja_id: int, classe_loja_atualizacao: LodgeClassUpdate):
    """Atualiza uma classe de loja existente no banco de dados."""
    db_classe_loja = obter_classe_loja_por_id(db, classe_loja_id)
    
    update_data = classe_loja_atualizacao.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_classe_loja, key, value)

    db.add(db_classe_loja)
    db.commit()
    db.refresh(db_classe_loja)
    return db_classe_loja

def deletar_classe_loja(db: Session, classe_loja_id: int):
    """Deleta uma classe de loja do banco de dados."""
    db_classe_loja = obter_classe_loja_por_id(db, classe_loja_id)
    db.delete(db_classe_loja)
    db.commit()
    return {"mensagem": "Classe de Loja deletada com sucesso."}
