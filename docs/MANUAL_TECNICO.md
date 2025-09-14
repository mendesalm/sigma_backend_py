# Manual Técnico: SiGMa Backend Python

**Última atualização:** 14 de Setembro de 2025

Este documento fornece uma visão técnica aprofundada do backend do SiGMa (Sistema de Gestão de Lojas Maçônicas), implementado em Python com FastAPI. O objetivo é detalhar a arquitetura, estrutura de dados, regras de negócio e o processo de implantação, permitindo que novos desenvolvedores compreendam e recriem o ambiente do projeto.

## 1. Visão Geral e Arquitetura

O backend é uma API RESTful construída com **FastAPI**, projetada para operar em um modelo **SaaS multi-tenant**.

- **Arquitetura Principal:** A aplicação segue um padrão de design com separação de responsabilidades:
    - **Controllers (`controllers/`):** Camada de API que lida com requisições HTTP, validação de entrada e orquestração da resposta.
    - **Services (`services/`):** Camada de serviço que encapsula toda a lógica de negócio.
    - **Models (`models/`):** Camada de acesso a dados, definida com SQLAlchemy ORM, que mapeia objetos Python para tabelas do banco de dados.
    - **Schemas (`schemas/`):** Camada de contrato de dados (DTOs) usando Pydantic, que define a estrutura das requisições e respostas da API.

- **Multi-Tenancy:** O sistema utiliza uma arquitetura de **Banco de Dados Único com Esquema Compartilhado**. Todos os dados residem em um único banco de dados, e a separação dos dados de cada Loja (tenant) é garantida a nível de aplicação, principalmente através de uma coluna `id_loja` em tabelas de dados de tenant.

- **Stack Tecnológica:**
    - **Framework:** FastAPI
    - **ORM:** SQLAlchemy
    - **Migrações de Banco de Dados:** Alembic
    - **Validação de Dados:** Pydantic
    - **Autenticação:** JSON Web Tokens (JWT) com `python-jose` e `bcrypt`
    - **Configuração:** `pydantic-settings` para gerenciamento de variáveis de ambiente (`.env`)
    - **Servidor ASGI:** Uvicorn

## 2. Estrutura de Diretórios

```
backend_python/
├── alembic/                   # Arquivos de migração do Alembic.
│   └── versions/
├── config/                    # Módulos de configuração.
│   └── settings.py            # Carrega e valida variáveis de ambiente com Pydantic.
├── controllers/               # Roteadores da API, separados por contexto (global, tenant).
├── database/                  # Configuração da conexão com o banco de dados.
│   └── connection.py
├── docs/                      # Documentação do projeto.
├── middleware/                # Middlewares customizados (ex: autorização).
├── models/                    # Definições dos modelos de dados (SQLAlchemy).
│   └── models.py
├── schemas/                   # Definições dos schemas (Pydantic) para a API.
├── services/                  # Lógica de negócio da aplicação.
├── utils/                     # Funções utilitárias (ex: logger, auth).
├── .env                       # Arquivo de variáveis de ambiente (NÃO versionado).
├── .gitignore                 # Arquivos e pastas a serem ignorados pelo Git.
├── main.py                    # Ponto de entrada da aplicação FastAPI.
└── requirements.txt           # Dependências do projeto.
```

## 3. Modelo de Dados Detalhado

O esquema do banco de dados é definido em `models/models.py`. Abaixo estão as tabelas principais:

| Tabela | Propósito |
|---|---|
| `super_administradores` | Armazena os usuários globais que gerenciam o sistema. |
| `classes` | Define os tipos de entidades (ex: Potência Federal, Potência Estadual, Loja Simbólica). |
| `lojas` | Tabela central de tenants. Cada registro é uma Loja, Potência Estadual ou Federal. |
| `webmasters` | Contas de administrador para cada `Loja`. Criado durante o onboarding da loja. |
| `membros_loja` | Registros de membros pertencentes a uma `Loja` específica. |
| `cargos` | Define os papéis ou funções que um membro pode ter (ex: Venerável Mestre, Secretário). |
| `permissoes` | Define ações específicas que podem ser permitidas ou negadas (ex: `criar_usuario`, `editar_tesouraria`). |
| `cargos_permissoes` | Tabela de associação que vincula `Cargos` a `Permissoes` (implementa o RBAC). |
| `associacoes_membros_loja` | Vincula um `MembroLoja` a um `Cargo`. |
| `hierarquia_lojas` | Modela a estrutura hierárquica entre as entidades da tabela `lojas`. |
| `processos_administrativos` | Exemplo de tabela de dados específica de um tenant. |

## 4. Atores e Regras de Negócio

O sistema possui uma hierarquia clara de usuários e entidades.

- **Atores:**
    1.  **SuperAdministrador:** O administrador geral do sistema. Tem acesso irrestrito e é responsável por criar e gerenciar as `Lojas` (tenants). O acesso às suas funcionalidades é protegido por middleware.
    2.  **Webmaster:** O administrador de uma `Loja` específica. Esta conta é criada automaticamente durante o "onboarding" da loja. O Webmaster é responsável por configurar a loja e cadastrar os membros e cargos iniciais.
    3.  **MembroLoja:** Um membro regular de uma loja, com permissões definidas pelo `Cargo` que ocupa.

- **Regras de Negócio Chave:**
    - **Onboarding de Tenant:** O processo de criação de uma nova `Loja` é uma operação atômica realizada por um SuperAdministrador. Esta operação:
        1.  Cria o registro da `Loja` na tabela `lojas`.
        2.  Cria a conta do `Webmaster` associado na tabela `webmasters`.
        3.  Define as relações hierárquicas da nova `Loja` na tabela `hierarquia_lojas`.
    - **Autenticação e Autorização:** O acesso à API é controlado por JWT. Endpoints globais (como o gerenciamento de tenants) são protegidos para serem acessíveis apenas por SuperAdministradores.

## 5. Guia de Instalação e Execução

Siga estes passos para configurar e executar o ambiente de desenvolvimento local.

### Passo 1: Pré-requisitos
- Git
- Python 3.10 ou superior
- Acesso a um servidor de banco de dados MySQL.

### Passo 2: Clonar e Preparar o Ambiente
```bash
# Clone o repositório (se ainda não o fez)
# git clone https://github.com/mendesalm/sigma_backend_py.git
# cd sigma_backend_py

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
# source venv/bin/activate
```

### Passo 3: Instalar Dependências
Com o ambiente virtual ativado, instale as dependências listadas em `requirements.txt`.
```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz da pasta `backend_python`. Use o template abaixo e preencha com suas credenciais.

```dotenv
# backend_python/.env

# --- Ambiente ---
NODE_ENV=development
PORT=8000

# --- Banco de Dados ---
DB_GLOBAL_HOST=localhost
DB_GLOBAL_PORT=3306
DB_GLOBAL_NAME=sigma_data
DB_GLOBAL_USER=seu_usuario_mysql
DB_GLOBAL_PASS=sua_senha_mysql
DB_DIALECT=mysql

# --- JWT ---
# Gere uma chave segura de 32 caracteres ou mais.
# Exemplo: openssl rand -hex 32
JWT_SECRET=sua_chave_secreta_super_longa_e_segura_de_32_caracteres
JWT_EXPIRES_IN=24h

# --- Email (Exemplo) ---
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=user@example.com
EMAIL_PASS=secret
```

### Passo 5: Configurar o Banco de Dados
1.  **Crie o Banco de Dados:** Certifique-se de que o banco de dados (`sigma_data` no exemplo acima) exista no seu servidor MySQL.
2.  **Execute as Migrações:** O Alembic gerencia o esquema do banco de dados. Para aplicar todas as migrações e criar/atualizar as tabelas, execute:
    ```bash
    # A partir da raiz do projeto (c:/sigma)
    alembic upgrade head
    ```

### Passo 6: Executar a Aplicação
Com tudo configurado, inicie o servidor Uvicorn. O comando deve ser executado de dentro da pasta `backend_python`.

```bash
cd backend_python
uvicorn main:aplicacao --reload
```

- `--reload`: Faz com que o servidor reinicie automaticamente após alterações no código.

A API estará disponível em `http://127.0.0.1:8000`.
A documentação interativa (Swagger UI) estará em `http://127.0.0.1:8000/docs`.
