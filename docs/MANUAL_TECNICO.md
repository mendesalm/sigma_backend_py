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
| `membros_loja` | Registros de membros pertencentes a uma `Loja` específica. Contém dados pessoais, de contato e maçônicos. |
| `familiares` | Armazena os familiares associados a um `MembroLoja`. |
| `condecoracoes` | Armazena as condecorações e honrarias recebidas por um `MembroLoja`. |
| `historico_cargos` | Registra o histórico de cargos ocupados por um `MembroLoja`, com datas de início e término. |
| `cargos` | Define os papéis ou funções que um membro pode ter (ex: Venerável Mestre, Secretário). |
| `permissoes` | Define ações específicas que podem ser permitidas ou negadas (ex: `criar_usuario`, `editar_tesouraria`). |
| `cargos_permissoes` | Tabela de associação que vincula `Cargos` a `Permissoes` (implementa o RBAC). |
| `associacoes_membros_loja` | Vincula um `MembroLoja` a um `Cargo` atual. |
| `hierarquia_lojas` | Modela a estrutura hierárquica entre as entidades da tabela `lojas`. |
| `processos_administrativos` | Exemplo de tabela de dados específica de um tenant. |

## 4. Atores e Regras de Negócio

O sistema possui uma hierarquia clara de usuários e entidades.

- **Atores:**
    1.  **SuperAdministrador:** O administrador geral do sistema. Tem acesso irrestrito e é responsável por criar e gerenciar as `Lojas` (tenants).
    2.  **Webmaster:** O administrador de uma `Loja` específica. Esta conta é criada automaticamente durante o "onboarding" da loja e possui acesso total aos dados de seu tenant.
    3.  **MembroLoja:** Um membro regular de uma loja. Com a expansão recente, esta entidade agora pode ser um usuário com capacidade de login, cujas permissões são definidas pelo `Cargo` que ocupa.

- **Regras de Negócio Chave:**
    - **Onboarding de Tenant:** O processo de criação de uma nova `Loja` é uma operação atômica realizada por um SuperAdministrador.
    - **Autenticação e Autorização:** O acesso à API é controlado por JWT. O middleware `authorize_middleware.py` decodifica o token e identifica o perfil do usuário (`super_admin`, `webmaster`, `lodge_member`), aplicando as regras de permissão adequadas.

## 5. Gerenciamento de Membros (API)

A implementação recente expandiu significativamente o gerenciamento de membros. As operações são realizadas dentro do contexto de um tenant e são protegidas por autenticação.

- **Endpoints Principais:**
    - `POST /api/tenant/membros`: Cria um novo membro na loja.
    - `GET /api/tenant/membros`: Lista todos os membros da loja.
    - `GET /api/tenant/membros/{id}`: Obtém um membro específico.
    - `PUT /api/tenant/membros/{id}`: Atualiza um membro.
    - `DELETE /api/tenant/membros/{id}`: Deleta um membro.
- **Entidades Relacionadas:** Foram criados endpoints similares para gerenciar as entidades relacionadas, todos prefixados com `/api/tenant/`:
    - `/familiares`: Para CRUD de familiares.
    - `/condecoracoes`: Para CRUD de condecorações.
    - # Manual Técnico: SiGMa Backend Python

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
| `membros_loja` | Registros de membros pertencentes a uma `Loja` específica. Contém dados pessoais, de contato e maçônicos. |
| `familiares` | Armazena os familiares associados a um `MembroLoja`. |
| `condecoracoes` | Armazena as condecoracoes e honrarias recebidas por um `MembroLoja`. |
| `historico_cargos` | Registra o histórico de cargos ocupados por um `MembroLoja`, com datas de início e término. |
| `sessoes_maconicas` | Gerencia o agendamento e status das sessões maçônicas. |
| `lojas_externas` | Armazena informações de lojas não-clientes do sistema. |
| `visitantes` | Cadastro de maçons de lojas não-clientes que visitam sessões. |
| `presencas_sessao` | Registra a presença de `MembroLoja` ou `Visitante` em uma `SessaoMaconica`. |
| `cargos` | Define os papéis ou funções que um membro pode ter (ex: Venerável Mestre, Secretário). |
| `permissoes` | Define ações específicas que podem ser permitidas ou negadas (ex: `criar_usuario`, `editar_tesouraria`). |
| `cargos_permissoes` | Tabela de associação que vincula `Cargos` a `Permissoes` (implementa o RBAC). |
| `associacoes_membros_loja` | Vincula um `MembroLoja` a um `Cargo` atual. |
| `hierarquia_lojas` | Modela a estrutura hierárquica entre as entidades da tabela `lojas`. |
| `processos_administrativos` | Exemplo de tabela de dados específica de um tenant. |

## 4. Atores e Regras de Negócio

O sistema possui uma hierarquia clara de usuários e entidades.

- **Atores:**
    1.  **SuperAdministrador:** O administrador geral do sistema. Tem acesso irrestrito e é responsável por criar e gerenciar as `Lojas` (tenants).
    2.  **Webmaster:** O administrador de uma `Loja` específica. Esta conta é criada automaticamente durante o "onboarding" da loja e possui acesso total aos dados de seu tenant.
    3.  **MembroLoja:** Um membro regular de uma loja. Com a expansão recente, esta entidade agora pode ser um usuário com capacidade de login, cujas permissões são definidas pelo `Cargo` que ocupa.

- **Regras de Negócio Chave:**
    - **Onboarding de Tenant:** O processo de criação de uma nova `Loja` é uma operação atômica realizada por um SuperAdministrador.
    - **Autenticação e Autorização:** O acesso à API é controlado por JWT. O middleware `authorize_middleware.py` decodifica o token e identifica o perfil do usuário (`super_admin`, `webmaster`, `lodge_member`), aplicando as regras de permissão adequadas.

## 5. Gerenciamento de Membros (API)

A implementação recente expandiu significativamente o gerenciamento de membros. As operações são realizadas dentro do contexto de um tenant e são protegidas por autenticação.

- **Endpoints Principais:**
    - `POST /api/tenant/membros`: Cria um novo membro na loja.
    - `GET /api/tenant/membros`: Lista todos os membros da loja.
    - `GET /api/tenant/membros/{id}`: Obtém um membro específico.
    - `PUT /api/tenant/membros/{id}`: Atualiza um membro.
    - `DELETE /api/tenant/membros/{id}`: Deleta um membro.
- **Entidades Relacionadas:** Foram criados endpoints similares para gerenciar as entidades relacionadas, todos prefixados com `/api/tenant/`:
    - `/familiares`: Para CRUD de familiares.
    - `/condecoracoes`: Para CRUD de condecoracoes.
    - `/historico-cargos`: Para CRUD do histórico de cargos.

## 6. Gerenciamento de Sessões Maçônicas (API)

Esta seção detalha a funcionalidade de gerenciamento de sessões, incluindo agendamento, status e registro de presença.

- **Modelos de Dados Principais:**
    - `SessaoMaconica`: Representa uma sessão agendada ou realizada.
    - `LojaExterna`: Informações sobre lojas que não são clientes do sistema.
    - `Visitante`: Maçons de lojas externas que podem participar de sessões.
    - `PresencaSessao`: Registro da presença de `MembroLoja` ou `Visitante` em uma `SessaoMaconica`. 

- **Regras de Negócio Chave:**
    - **Tipos e Subtipos de Sessão:** As sessões são classificadas por `tipo` (Ordinária, Magna, Extraordinária) e `subtipo` (detalhado no código).
    - **Ciclo de Vida do Status:** As sessões progridem por status (`Agendada`, `Em Andamento`, `Realizada`, `Cancelada`). A atualização é manual via API.
    - **Sugestão de Agendamento:** Um endpoint pode sugerir a próxima data e hora da sessão com base na periodicidade da loja.
    - **Registro de Presença:**
        - **Manual:** Chanceler (ou usuário com permissão específica) pode registrar presenças via API.
        - **Automático (Check-in):** Um endpoint `checkin` permite que membros e visitantes registrem presença via QR Code dentro de uma janela de tempo específica (2h antes a 2h depois do início da sessão).

- **Endpoints Principais:**
    - `POST /api/tenant/sessoes`: Cria uma nova sessão.
    - `GET /api/tenant/sessoes`: Lista sessões da loja.
    - `GET /api/tenant/sessoes/{id}`: Obtém detalhes de uma sessão.
    - `PUT /api/tenant/sessoes/{id}`: Atualiza dados de uma sessão.
    - `DELETE /api/tenant/sessoes/{id}`: Deleta uma sessão.
    - `PUT /api/tenant/sessoes/{id}/status`: Atualiza o status da sessão.
    - `GET /api/tenant/sessoes/sugerir-proxima`: Sugere a próxima data de sessão.
    - `POST /api/tenant/presencas`: Registra presença manual.
    - `GET /api/tenant/presencas/sessao/{sessao_id}`: Lista presenças de uma sessão.
    - `DELETE /api/tenant/presencas/{id}`: Deleta registro de presença.
    - `POST /api/tenant/presencas/checkin`: Endpoint para check-in via QR Code.
    - `POST /api/global/lojas-externas`: CRUD para Lojas Externas (global).
    - `POST /api/global/visitantes`: CRUD para Visitantes (global).

## 7. Guia de Instalação e Execução

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


## 6. Guia de Instalação e Execução

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
