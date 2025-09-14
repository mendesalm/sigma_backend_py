# backend_python/services/sessao_maconica_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta, time
from typing import Optional

from models.models import SessaoMaconica, Loja
from schemas.sessao_maconica_schema import SessaoMaconicaCreate, SessaoMaconicaUpdate, StatusSessao

# Mapeamento de dias da semana para números (0=Segunda, 6=Domingo)
dias_semana_map = {
    'Segunda-feira': 0,
    'Terça-feira': 1,
    'Quarta-feira': 2,
    'Quinta-feira': 3,
    'Sexta-feira': 4,
    'Sábado': 5,
    'Domingo': 6
}

def create_sessao(db: Session, sessao_data: SessaoMaconicaCreate) -> SessaoMaconica:
    """Cria uma nova sessão maçônica no banco de dados."""
    # Valida se a loja existe
    loja = db.query(Loja).filter(Loja.id == sessao_data.id_loja).first()
    if not loja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Loja com id {sessao_data.id_loja} não encontrada.")

    nova_sessao = SessaoMaconica(**sessao_data.model_dump())
    db.add(nova_sessao)
    db.commit()
    db.refresh(nova_sessao)
    return nova_sessao

def get_sessao_by_id(db: Session, sessao_id: int) -> SessaoMaconica:
    """Busca uma sessão maçônica pelo seu ID."""
    sessao = db.query(SessaoMaconica).filter(SessaoMaconica.id == sessao_id).first()
    if not sessao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sessão não encontrada.")
    return sessao

def get_all_sessoes_from_loja(db: Session, loja_id: int, skip: int = 0, limit: int = 100):
    """Lista todas as sessões de uma loja específica."""
    return db.query(SessaoMaconica).filter(SessaoMaconica.id_loja == loja_id).offset(skip).limit(limit).all()

def update_sessao(db: Session, sessao_id: int, sessao_data: SessaoMaconicaUpdate) -> SessaoMaconica:
    """Atualiza os dados de uma sessão maçônica."""
    db_sessao = get_sessao_by_id(db, sessao_id)

    update_data = sessao_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sessao, key, value)

    db.commit()
    db.refresh(db_sessao)
    return db_sessao

def delete_sessao(db: Session, sessao_id: int):
    """Deleta uma sessão maçônica do banco de dados."""
    db_sessao = get_sessao_by_id(db, sessao_id)
    db.delete(db_sessao)
    db.commit()
    return {"ok": True}

def update_sessao_status(db: Session, sessao_id: int, new_status: StatusSessao) -> SessaoMaconica:
    """Atualiza o status de uma sessão maçônica."""
    db_sessao = get_sessao_by_id(db, sessao_id)
    db_sessao.status = new_status
    db.commit()
    db.refresh(db_sessao)
    return db_sessao

def suggest_next_session_date(db: Session, loja_id: int) -> Optional[datetime]:
    """Sugere a próxima data e hora de sessão para uma loja com base em sua periodicidade."""
    loja = db.query(Loja).filter(Loja.id == loja_id).first()
    if not loja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Loja com id {loja_id} não encontrada.")

    if not loja.dia_sessoes or not loja.hora_sessao or not loja.periodicidade:
        return None # Não é possível sugerir sem dados de periodicidade

    # Converte o dia da semana para número (0=Segunda, 6=Domingo)
    target_weekday = dias_semana_map.get(loja.dia_sessoes)
    if target_weekday is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dia da semana configurado para a loja é inválido.")

    # Busca a última sessão realizada para esta loja
    ultima_sessao = db.query(SessaoMaconica).filter(
        SessaoMaconica.id_loja == loja_id,
        SessaoMaconica.status == StatusSessao.REALIZADA # Ou outro status que indique sessão concluída
    ).order_by(SessaoMaconica.data_hora_inicio.desc()).first()

    # Define o ponto de partida para a busca da próxima data
    if ultima_sessao:
        start_date = ultima_sessao.data_hora_inicio.date()
    else:
        start_date = datetime.now().date() # Começa a partir de hoje se não houver sessões anteriores

    # Calcula a próxima data baseada na periodicidade
    next_date = start_date
    found_next_date = False

    while not found_next_date:
        next_date += timedelta(days=1) # Avança um dia por vez
        
        if next_date.weekday() == target_weekday:
            if loja.periodicidade == 'Semanal':
                found_next_date = True
            elif loja.periodicidade == 'Quinzenal':
                # Para quinzenal, verifica se a diferença em semanas é ímpar
                # Isso é uma simplificação, pode precisar de lógica mais robusta
                if ultima_sessao and (next_date - ultima_sessao.data_hora_inicio.date()).days % 14 == 0:
                    found_next_date = True
                elif not ultima_sessao and (next_date - start_date).days % 14 == 0:
                    found_next_date = True
            elif loja.periodicidade == 'Mensal':
                # Para mensal, verifica se é o mesmo dia do mês ou uma lógica mais complexa
                # Por simplicidade, vamos sugerir o próximo dia da semana alvo no próximo mês
                if next_date.month != start_date.month and next_date.day >= start_date.day:
                    found_next_date = True
                elif next_date.month == start_date.month and next_date.day > start_date.day and next_date.weekday() == target_weekday:
                    found_next_date = True

    # Combina a data calculada com a hora da sessão da loja
    suggested_datetime = datetime.combine(next_date, loja.hora_sessao)

    # Garante que a data sugerida não seja no passado
    if suggested_datetime < datetime.now():
        # Se for no passado, recalcula a partir de hoje
        return suggest_next_session_date(db, loja_id) # Chamada recursiva para encontrar a próxima a partir de hoje

    return suggested_datetime
