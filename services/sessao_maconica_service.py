# backend_python/services/sessao_maconica_service.py

from sqlalchemy.orm import Session
from models import models
from schemas import sessao_maconica_schema, presenca_sessao_schema, visitante_schema
from datetime import datetime, timedelta

def get_sessoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SessaoMaconica).offset(skip).limit(limit).all()

def get_sessao(db: Session, sessao_id: int):
    return db.query(models.SessaoMaconica).filter(models.SessaoMaconica.id == sessao_id).first()

def create_sessao(db: Session, sessao: sessao_maconica_schema.SessaoMaconicaCreate, loja_id: int):
    db_sessao = models.SessaoMaconica(**sessao.dict(), id_loja=loja_id)
    db.add(db_sessao)
    db.commit()
    db.refresh(db_sessao)

    membros_ativos = db.query(models.MembroLoja).filter(models.MembroLoja.id_loja == loja_id, models.MembroLoja.situacao == 'Ativo').all()
    for membro in membros_ativos:
        presenca = presenca_sessao_schema.PresencaSessaoCreate(id_sessao=db_sessao.id, id_membro=membro.id, status_presenca='Ausente')
        db_presenca = models.PresencaSessao(**presenca.dict())
        db.add(db_presenca)
    
    db.commit()
    db.refresh(db_sessao)

    return db_sessao

def update_session_attendance(db: Session, sessao_id: int, attendance_data: list[presenca_sessao_schema.PresencaSessaoBase]):
    for attendance in attendance_data:
        db.query(models.PresencaSessao).filter(
            models.PresencaSessao.id_sessao == sessao_id,
            models.PresencaSessao.id_membro == attendance.id_membro
        ).update({"status_presenca": attendance.status_presenca})
    db.commit()
    return get_sessao(db, sessao_id)

def manage_session_visitor(db: Session, sessao_id: int, visitor_data: visitante_schema.VisitanteCreate):
    db_visitor = models.Visitante(**visitor_data.dict(), id_sessao=sessao_id)
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor

def remove_session_visitor(db: Session, visitor_id: int):
    db_visitor = db.query(models.Visitante).filter(models.Visitante.id == visitor_id).first()
    if db_visitor:
        db.delete(db_visitor)
        db.commit()
    return db_visitor

def suggest_next_session_date(db: Session, loja_id: int):
    loja = db.query(models.Loja).filter(models.Loja.id == loja_id).first()
    if not loja:
        return None

    last_session = db.query(models.SessaoMaconica).filter(models.SessaoMaconica.id_loja == loja_id).order_by(models.SessaoMaconica.data_sessao.desc()).first()

    if last_session:
        last_date = last_session.data_sessao
    else:
        last_date = datetime.now()

    if loja.periodicidade == 'Semanal':
        next_date = last_date + timedelta(weeks=1)
    elif loja.periodicidade == 'Quinzenal':
        next_date = last_date + timedelta(weeks=2)
    elif loja.periodicidade == 'Mensal':
        next_date = last_date + timedelta(days=30) # This is a simplification, a more robust solution should be implemented
    else:
        return None

    # This is a simplification. A more robust solution should consider the specific day of the week.
    return next_date
