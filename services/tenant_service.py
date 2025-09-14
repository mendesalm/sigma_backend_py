# backend_python/services/tenant_service.py

from sqlalchemy.orm import Session
from models.models import Loja, Webmaster, HierarquiaLoja, ClasseLoja
from schemas.tenant_schema import TenantCreate, TenantUpdate
from fastapi import HTTPException, status
import bcrypt
import secrets # Para gerar chaves de API
import json # Para lidar com campos JSON

def criar_loja(db: Session, dados_loja: TenantCreate):
    """Cria uma nova loja (tenant), seu webmaster e associações hierárquicas."""
    # 1. Validar lodge_code único
    if db.query(Loja).filter(Loja.codigo_loja == dados_loja.codigo_loja).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Código da loja já existe.")

    # 2. Validar id_classe_loja
    if dados_loja.id_classe_loja:
        classe_loja = db.query(ClasseLoja).filter(ClasseLoja.id == dados_loja.id_classe_loja).first()
        if not classe_loja:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classe de Loja não encontrada.")

    # 3. Gerar chaves de API (exemplo simples)
    chaves_api = {
        "public_key": secrets.token_urlsafe(16),
        "private_key": secrets.token_urlsafe(32)
    }

    # 4. Criar a Loja
    nova_loja = Loja(
        codigo_loja=dados_loja.codigo_loja,
        numero_loja=dados_loja.numero_loja,
        nome_loja=dados_loja.nome_loja,
        titulo_loja=dados_loja.titulo_loja,
        obediencia_loja=dados_loja.obediencia_loja,
        id_classe_loja=dados_loja.id_classe_loja,
        dominio_personalizado=dados_loja.dominio_personalizado,
        plano=dados_loja.plano,
        limite_usuarios=dados_loja.limite_usuarios,
        configuracoes_globais=json.dumps(dados_loja.configuracoes_globais), # Armazena como JSON string
        chaves_api=json.dumps(chaves_api), # Armazena como JSON string
        esta_ativo=dados_loja.esta_ativo,
        status=dados_loja.status,
        dia_sessoes=dados_loja.dia_sessoes,
        periodicidade=dados_loja.periodicidade,
        hora_sessao=dados_loja.hora_sessao
    )
    db.add(nova_loja)
    db.commit()
    db.refresh(nova_loja)

    # 5. Criar o Webmaster
    senha_hash_webmaster = bcrypt.hashpw(dados_loja.senha_webmaster.encode('utf-8'), bcrypt.gensalt())
    novo_webmaster = Webmaster(
        id_loja=nova_loja.id,
        nome_usuario=f"webmaster_{dados_loja.codigo_loja}", # Nome de usuário padrão
        email=dados_loja.email_webmaster,
        senha_hash=senha_hash_webmaster.decode('utf-8'),
        esta_ativo=True
    )
    db.add(novo_webmaster)
    db.commit()
    db.refresh(novo_webmaster)

    # 6. Criar Hierarquia (se houver superiorLodges)
    for superior_id in dados_loja.superior_lodges:
        superior_loja = db.query(Loja).filter(Loja.id == superior_id).first()
        if not superior_loja:
            # Opcional: levantar erro ou apenas ignorar IDs inválidos
            print(f"Aviso: Loja superior com ID {superior_id} não encontrada. Ignorando associação hierárquica.")
            continue
        
        nova_hierarquia = HierarquiaLoja(
            superior_lodge_id=superior_id,
            subordinate_lodge_id=nova_loja.id,
            relationship_type="subordinada" # Tipo de relacionamento padrão
        )
        db.add(nova_hierarquia)
    db.commit()

    # Retorna a loja criada (e o webmaster pode ser retornado separadamente se necessário)
    return nova_loja

def obter_todas_lojas(db: Session):
    """Retorna todas as lojas (tenants) do banco de dados."""
    return db.query(Loja).all()

def obter_loja_por_id(db: Session, loja_id: int):
    """Retorna uma loja específica pelo ID."""
    loja = db.query(Loja).filter(Loja.id == loja_id).first()
    if not loja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada.")
    return loja

def atualizar_loja(db: Session, loja_id: int, loja_atualizacao: TenantUpdate):
    """Atualiza as informações de uma loja existente no banco de dados."""
    db_loja = obter_loja_por_id(db, loja_id)
    
    update_data = loja_atualizacao.model_dump(exclude_unset=True)
    
    # Lidar com campos JSON
    if "configuracoes_globais" in update_data:
        update_data["configuracoes_globais"] = json.dumps(update_data["configuracoes_globais"])
    if "chaves_api" in update_data:
        update_data["chaves_api"] = json.dumps(update_data["chaves_api"])

    for key, value in update_data.items():
        setattr(db_loja, key, value)

    db.add(db_loja)
    db.commit()
    db.refresh(db_loja)
    return db_loja

def deletar_loja(db: Session, loja_id: int):
    """Deleta uma loja do banco de dados."""
    db_loja = obter_loja_por_id(db, loja_id)
    db.delete(db_loja)
    db.commit()
    return {"mensagem": "Loja deletada com sucesso."}
