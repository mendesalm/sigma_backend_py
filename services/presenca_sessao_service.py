# backend_python/services/presenca_sessao_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from models.models import PresencaSessao, SessaoMaconica, MembroLoja, Visitante
from schemas.presenca_sessao_schema import PresencaSessaoCreate
from . import sessao_maconica_service
from . import membro_service
from . import visitante_service

def create_presenca(db: Session, presenca_data: PresencaSessaoCreate) -> PresencaSessao:
    """Cria um novo registro de presença para uma sessão."""
    # Valida se a sessão existe
    sessao_maconica_service.get_sessao_by_id(db, presenca_data.id_sessao)

    # Valida se id_membro ou id_visitante é fornecido e válido
    if presenca_data.id_membro and presenca_data.id_visitante:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Apenas um entre id_membro ou id_visitante deve ser fornecido.")
    elif presenca_data.id_membro:
        membro_service.get_membro_by_id(db, presenca_data.id_membro)
    elif presenca_data.id_visitante:
        visitante_service.get_visitante_by_id(db, presenca_data.id_visitante)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pelo menos um entre id_membro ou id_visitante deve ser fornecido.")

    # Verifica se a presença já foi registrada para este membro/visitante nesta sessão
    query = db.query(PresencaSessao).filter(PresencaSessao.id_sessao == presenca_data.id_sessao)
    if presenca_data.id_membro:
        query = query.filter(PresencaSessao.id_membro == presenca_data.id_membro)
    elif presenca_data.id_visitante:
        query = query.filter(PresencaSessao.id_visitante == presenca_data.id_visitante)
    
    if query.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Presença já registrada para esta sessão e participante.")

    nova_presenca = PresencaSessao(**presenca_data.model_dump())
    db.add(nova_presenca)
    db.commit()
    db.refresh(nova_presenca)
    return nova_presenca

def get_presenca_by_id(db: Session, presenca_id: int) -> PresencaSessao:
    """Busca um registro de presença pelo seu ID."""
    presenca = db.query(PresencaSessao).filter(PresencaSessao.id == presenca_id).first()
    if not presenca:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de presença não encontrado.")
    return presenca

def get_all_presencas_from_sessao(db: Session, sessao_id: int, skip: int = 0, limit: int = 100):
    """Lista todos os registros de presença de uma sessão específica."""
    return db.query(PresencaSessao).filter(PresencaSessao.id_sessao == sessao_id).offset(skip).limit(limit).all()

def delete_presenca(db: Session, presenca_id: int):
    """Deleta um registro de presença do banco de dados."""
    db_presenca = get_presenca_by_id(db, presenca_id)
    db.delete(db_presenca)
    db.commit()
    return {"ok": True}

def checkin_presenca(db: Session, sessao_id: int, id_loja_qr_code: int, current_user: dict) -> PresencaSessao:
    """Processa o check-in de presença via QR Code para uma sessão."""
    sessao = sessao_maconica_service.get_sessao_by_id(db, sessao_id)

    # 1. Valida se a sessão pertence à loja do QR Code
    if sessao.id_loja != id_loja_qr_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sessão não pertence à loja do QR Code.")

    # 2. Valida a janela de tempo (2 horas antes e 2 horas depois do início da sessão)
    now = datetime.now()
    janela_inicio = sessao.data_hora_inicio - timedelta(hours=2)
    janela_fim = sessao.data_hora_inicio + timedelta(hours=2)

    if not (janela_inicio <= now <= janela_fim):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Check-in fora da janela de tempo permitida.")

    # 3. Identifica o participante (membro ou visitante)
    id_membro = None
    id_visitante = None
    perfil = current_user.get("perfil")

    if perfil == "lodge_member":
        id_membro = current_user["user"].id
        # Opcional: Valida se o membro pertence à loja da sessão (se for o caso de check-in em loja própria)
        if current_user["tenant"].id != sessao.id_loja:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Membro não pertence a esta loja.")

    elif perfil == "visitante": # Assumindo que visitantes terão um perfil JWT próprio após o cadastro
        id_visitante = current_user["user"].id
        # Opcional: Valida se o visitante está tentando fazer check-in em uma sessão de sua loja de origem, se aplicável

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Perfil de usuário não autorizado para check-in.")

    # 4. Cria o registro de presença
    presenca_data = PresencaSessaoCreate(
        id_sessao=sessao_id,
        id_membro=id_membro,
        id_visitante=id_visitante
    )
    return create_presenca(db, presenca_data)
