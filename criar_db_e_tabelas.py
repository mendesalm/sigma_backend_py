from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from database import Base, engine, DATABASE_URL
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DB_USER = os.getenv("DB_GLOBAL_USER")
DB_PASS = quote_plus(os.getenv("DB_GLOBAL_PASS"))
DB_HOST = os.getenv("DB_GLOBAL_HOST")
DB_PORT = os.getenv("DB_GLOBAL_PORT")
DB_NAME = os.getenv("DB_GLOBAL_NAME")

# Constrói uma string de conexão sem o nome do banco de dados para criá-lo
# Isso é necessário porque create_database precisa se conectar ao servidor primeiro
SERVER_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/"
server_engine = create_engine(SERVER_URL)

if not database_exists(DATABASE_URL):
    print(f"Criando o banco de dados {DB_NAME}...")
    create_database(DATABASE_URL)
    print(f"Banco de dados {DB_NAME} criado.")
else:
    print(f"Banco de dados {DB_NAME} já existe.")

print("Criando tabelas...")
Base.metadata.create_all(engine)
print("Tabelas criadas com sucesso.")
