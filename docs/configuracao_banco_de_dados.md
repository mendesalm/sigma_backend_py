# Configuração e Gerenciamento do Banco de Dados (Backend Python)

Este documento detalha o processo de configuração e gerenciamento do banco de dados para o backend da aplicação, implementado em Python.

## Pré-requisitos

Certifique-se de ter um servidor MySQL instalado e em execução em sua máquina local ou em um ambiente acessível.

## Configuração do Banco de Dados

O backend utiliza variáveis de ambiente para a configuração do banco de dados. Crie um arquivo `.env` na raiz do diretório `backend_python/` com as seguintes variáveis:

```
DB_GLOBAL_HOST=localhost
DB_GLOBAL_PORT=3306
DB_GLOBAL_USER=root
DB_GLOBAL_PASS=your_mysql_password
DB_GLOBAL_NAME=sigma_data
```

- `DB_GLOBAL_HOST`: Host do seu servidor MySQL.
- `DB_GLOBAL_PORT`: Porta do seu servidor MySQL (padrão: 3306).
- `DB_GLOBAL_USER`: Nome de usuário do MySQL.
- `DB_GLOBAL_PASS`: Senha do usuário do MySQL.
- `DB_GLOBAL_NAME`: Nome do banco de dados principal da aplicação (ex: `sigma_data`).

## Criação do Banco de Dados e Tabelas

Para criar o banco de dados e todas as tabelas definidas nos modelos SQLAlchemy, você pode executar o script `create_db_and_tables.py`.

Execute o seguinte comando na raiz do diretório `backend_python/`: 

```bash
python create_db_and_tables.py
```

Este script verificará se o banco de dados existe e o criará se necessário. Em seguida, ele criará todas as tabelas definidas nos modelos SQLAlchemy.

## Gerenciamento de Migrações

Atualmente, a criação do esquema do banco de dados é feita via `Base.metadata.create_all()` no script `create_db_and_tables.py` e no evento de startup do `main.py`.

Para um gerenciamento de esquema mais robusto e para lidar com alterações futuras no banco de dados em ambientes de produção, é **altamente recomendado** implementar um sistema de migrações, como o **Alembic**.

## Seeders

(Esta seção será detalhada conforme a implementação de seeders em Python for avançando.)
