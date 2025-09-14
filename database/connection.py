# backend_python/database/connection.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import config  # Importa a configuração centralizada

# Cria o engine do SQLAlchemy usando a URL do arquivo de configuração
engine = create_engine(config.URL_BANCO_DE_DADOS)

# Cria uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe Base para os modelos declarativos
Base = declarative_base()

# Dependência do FastAPI para obter a sessão do banco de dados
def get_db():
    """
    Cria e fornece uma sessão de banco de dados por requisição.
    Garante que a sessão seja sempre fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
