# Manual Técnico - Backend SiGMa (Python)

## 1. Visão Geral

Este documento detalha a arquitetura, configuração e execução do backend do sistema SiGMa, desenvolvido em Python com o framework FastAPI.

## 2. Arquitetura e Tecnologias

- **Framework**: FastAPI, um framework web moderno e de alta performance para Python.
- **Banco de Dados**: A interação com o banco de dados é feita através do SQLAlchemy, um ORM (Object-Relational Mapper) robusto.
- **Migrações de Banco de Dados**: Gerenciadas pelo Alembic, garantindo a consistência do schema do banco de dados entre diferentes ambientes.
- **Validação de Dados**: Pydantic é usado para definir e validar os schemas de dados da API (requests e responses), garantindo a integridade dos dados.
- **Autenticação**: Baseada em tokens JWT (JSON Web Tokens).

## 3. Estrutura de Pastas

A estrutura do projeto foi organizada para separar as responsabilidades e facilitar a manutenção:

- `/config`: Gerencia as configurações da aplicação (`settings.py`).
- `/controllers`: Define os endpoints da API (rotas). A camada que lida com as requisições HTTP.
- `/database`: Gerencia a conexão com o banco de dados (`connection.py`).
- `/docs`: Contém a documentação do projeto.
- `/middleware`: Contém middlewares para processamento de requisições, como autenticação e identificação de tenant.
- `/models`: Define as tabelas do banco de dados como classes Python usando SQLAlchemy.
- `/schemas`: Contém os modelos Pydantic para validação de dados.
- `/services`: Contém a lógica de negócio da aplicação. Os controllers chamam os serviços para executar as tarefas.
- `/utils`: Funções utilitárias reutilizáveis (ex: criação de tokens, logging).

## 4. Configuração do Ambiente

O projeto requer um arquivo `.env` na raiz da pasta `backend_python` para configurar as variáveis de ambiente.

**Variáveis Essenciais:**

- `DB_DIALECT`: `mysql` ou `postgresql`.
- `DB_GLOBAL_HOST`: O host do banco de dados (ex: `127.0.0.1`).
- `DB_GLOBAL_PORT`: A porta do banco de dados (ex: `3306` para MySQL).
- `DB_GLOBAL_USER`: O nome de usuário do banco.
- `DB_GLOBAL_PASS`: A senha do banco. **Atenção:** Se a senha contiver caracteres especiais, ela será codificada automaticamente pelo sistema.
- `DB_GLOBAL_NAME`: O nome do banco de dados (ex: `sigma_data`).
- `JWT_SECRET`: Uma chave secreta longa (mínimo 32 caracteres) para assinar os tokens JWT.
- `ROOT_EMAIL`: E-mail para o super administrador inicial a ser criado pelo seeder.
- `ROOT_PASSWORD`: Senha para o super administrador inicial.
- `EMAIL_*`: Variáveis para configuração do servidor de e-mail (SMTP).

## 5. Guia de Instalação e Execução

Siga os passos abaixo para configurar e executar o ambiente de desenvolvimento do backend.

**Passo 1: Criar Ambiente Virtual e Instalar Dependências**

```bash
# Navegue até a pasta do backend
cd backend_python

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

**Passo 2: Configurar Banco de Dados e .env**

1.  Garanta que você tenha um servidor de banco de dados MySQL (ou PostgreSQL) em execução.
2.  Crie um banco de dados com o nome definido em `DB_GLOBAL_NAME` (ex: `CREATE DATABASE sigma_data;`).
3.  Crie o arquivo `.env` na pasta `backend_python` com todas as variáveis listadas na seção 4.

**Passo 3: Executar Migrações do Banco de Dados**

Com o ambiente virtual ativado e a partir da pasta raiz `sigma/`, execute o Alembic para criar as tabelas no banco:

```bash
alembic upgrade head
```

**Passo 4: Popular o Banco com Dados Iniciais (Seeding)**

Para criar o primeiro super administrador, execute o script de seed:

```bash
python backend_python/seed_db.py
```

**Passo 5: Iniciar o Servidor**

Finalmente, inicie o servidor FastAPI:

```bash
# A partir da pasta backend_python
uvicorn main:app --reload
```

O servidor estará disponível em `http://127.0.0.1:8000`.