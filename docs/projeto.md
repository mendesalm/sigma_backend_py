# Documentação Técnica: SiGMa Backend Python

**Última atualização:** 10 de Setembro de 2025

Este documento detalha a arquitetura, as convenções e os fluxos de trabalho do backend do Sistema Integrado de Gestão de Lojas Maçônicas (SiGMa), agora implementado em Python.

## 1. Visão Geral e Arquitetura

O backend é construído em **Python (FastAPI)** e projetado para operar em um modelo **SaaS multi-tenant** usando uma arquitetura de **Banco de Dados Único com Esquema Compartilhado (Single Database, Shared Schema)**.

Todos os dados, tanto globais quanto de tenants, residem em um único banco de dados (`sigma_db`). A separação e a segurança dos dados de cada Loja (tenant) são garantidas a nível de aplicação, utilizando uma coluna `tenant_id` em todas as tabelas relevantes. Esta abordagem simplifica a manutenção, as migrações e o deploy.

- **Banco de Dados Único (`sigma_db`):** Centraliza todos os dados do sistema. Tabelas que gerenciam o sistema (como `super_administradores` e `lojas`) operam globalmente, enquanto tabelas de negócio (como `membros_loja`) são filtradas por `tenant_id`.

### 1.1 Classes de Loja Dinâmicas e Hierarquia

Para atender à complexidade das organizações maçônicas, o sistema permite a definição dinâmica de **Classes de Loja** (ex: Federal, Estadual, Simbólica-RB, Simbólica-REAA, Filosófica-RB, Filosófica-REAA). Além disso, modela relações hierárquicas entre as lojas (ex: Obediências Estaduais subordinadas a Federais, Lojas Simbólicas jurisdicionadas a Estaduais e/ou federadas a Federais).

## 2. Stack Tecnológica

- **Backend:** Python, FastAPI
- **Banco de Dados:** MySQL com SQLAlchemy ORM
- **Autenticação:** JSON Web Tokens (JWT) com `python-jose`, hashing de senhas com `bcrypt`
- **Validação:** Pydantic (para modelos de requisição e resposta)
- **Variáveis de Ambiente:** `python-dotenv`
- **Migrations:** (A ser implementado, atualmente `Base.metadata.create_all()`)
- **Documentação da API:** Swagger UI (integrado ao FastAPI)
- **Logging:** (A ser implementado, Python `logging` module)
- **Segurança:** (A ser implementado, FastAPI security features)
- **Módulos:** Python modules

## 3. Estrutura de Pastas Principal

A estrutura de pastas é organizada para separar claramente as responsabilidades.

```
backend_python/
├── create_db_and_tables.py # Script para criar o DB e tabelas (uso em dev)
├── database.py             # Configuração do DB, modelos SQLAlchemy e sessão
├── main.py                 # Ponto de entrada da aplicação FastAPI e rotas principais
├── requirements.txt        # Dependências do projeto Python
├── docs/                   # Documentação do projeto (este arquivo)
├── venv/                   # Ambiente virtual Python
└── .env                    # Variáveis de ambiente
```

## 4. Esquema do Banco de Dados

Esta seção detalha as tabelas principais do banco de dados `sigma_db`.

### Tabela `super_administradores`
Armazena as credenciais dos administradores gerais do sistema.

### Tabela `classes_loja`
Permite a definição dinâmica de classes de lojas.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | INT | Identificador único |
| `nome` | VARCHAR(255) | Nome da classe (ex: Federal, Estadual, Simbólica-RB) |
| `descricao` | VARCHAR(255) | Descrição da classe |

### Tabela `lojas`
Contém o registro de cada loja (tenant) no sistema.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | INT | Identificador único |
| `codigo_loja` | VARCHAR(32) | Código único da loja, usado na URL e identificação. |
| `id_classe_loja` | INT | Chave estrangeira para `classes_loja.id`. |
| `dia_sessoes`| ENUM | Dia da semana em que ocorrem as sessões. |
| `periodicidade`    | ENUM | Periodicidade das sessões (semanal, quinzenal, mensal). |
| `hora_sessao`   | TIME | Horário das sessões. |
| `...` | `...` | Demais campos conforme o modelo `Loja` em `database.py`. |

### Tabela `webmasters`
Armazena as credenciais do administrador de cada loja (tenant).

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | INT | Identificador único |
| `id_loja` | INT | Chave estrangeira para a tabela `lojas`. |
| `...` | `...` | Demais campos conforme o modelo `Webmaster` em `database.py`. |

### Tabelas de Tenant (Ex: `membros_loja`, `associacoes_membros_loja`)
Contêm os dados de negócio de cada loja, filtrados por `id_loja` (equivalente a `tenant_id`).

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | INT | Identificador único |
| `id_loja` | INT | Chave estrangeira para a tabela `lojas`, usada para isolar os dados. |
| `...` | `...` | Demais campos. |

## 5. Controle de Acesso Baseado em Funções (RBAC) e Hierarquia

(Esta seção será detalhada conforme a implementação avançar, espelhando a lógica do backend Node.js para RBAC e hierarquia de lojas.)

## 6. Fluxo de Onboarding de Tenant (Criação de Loja)

(Esta seção será detalhada conforme a implementação avançar, espelhando a lógica do backend Node.js para onboarding de tenants.)

## 7. Migrations e Seeders

Atualmente, a criação do esquema do banco de dados é feita via `Base.metadata.create_all()` no script `create_db_and_tables.py` e no evento de startup do `main.py`. Para gerenciamento de esquema em produção, será necessário implementar um sistema de migrações (e.g., Alembic).

## 8. Documentação da API (Swagger UI)

O FastAPI gera documentação interativa da API automaticamente.

-   **Acesso:** A documentação estará disponível em tempo de desenvolvimento no endpoint `/docs` (ex: `http://localhost:8000/docs` se rodando na porta 8000).
-   **Geração:** A documentação é gerada automaticamente a partir das definições de rota e modelos Pydantic no código Python.
