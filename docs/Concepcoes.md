# Documento de Concepção: Funcionalidades em Desenvolvimento

Este documento serve como um registro vivo do planejamento e das decisões de design para as funcionalidades que estão sendo implementadas. Uma vez que uma funcionalidade é concluída, sua documentação é movida daqui para o `MANUAL_TECNICO.md`.

---

## **Em Andamento: Expansão do Gerenciamento de Membros**

**Objetivo:** Expandir as capacidades do sistema para incluir um gerenciamento detalhado dos membros da loja, seus familiares, honrarias recebidas e histórico de cargos, utilizando a implementação de referência em Node.js como guia.

### 1. Análise e Decisões de Design

Após análise dos arquivos de modelo (`.model.js`) da referência, as seguintes decisões de design foram tomadas para a implementação em Python/SQLAlchemy:

#### 1.1. Modelo de Membros (`MembroLoja`)
- **Decisão:** O modelo `MembroLoja` existente será drasticamente expandido para incluir os campos detalhados de dados pessoais, de contato e maçônicos presentes na referência.
- **Implicação:** Serão adicionados campos como `CPF`, `DataNascimento`, `Endereco_Rua`, `Graduacao`, `DataIniciacao`, etc.
- **Nota Arquitetural:** A adição de um campo `senha_hash` e campos relacionados à autenticação transformará `MembroLoja` em uma entidade capaz de realizar login, uma evolução do seu estado atual de apenas um registro de dados. A lógica de autenticação será implementada na camada de serviço correspondente.

#### 1.2. Modelos Adicionais (`Familiar`, `Condecoracao`)
- **Decisão:** Serão criados dois novos modelos, `Familiar` e `Condecoracao`.
- **Estrutura:** Eles conterão os campos identificados na análise (ex: `parentesco` para `Familiar`, `titulo` para `Condecoracao`) e terão um relacionamento de chave estrangeira direto com a tabela `membros_loja`.

#### 1.3. Modelo de Histórico de Cargos (`HistoricoCargo`)
- **Decisão:** Será criado o modelo `HistoricoCargo` para rastrear os cargos ocupados.
- **Melhoria de Design:** Diferente da referência, que usava um campo `ENUM` com nomes de cargos fixos, nossa implementação utilizará uma **chave estrangeira** para a tabela `cargos` já existente. 
- **Vantagem:** Esta abordagem relacional é mais flexível e robusta, permitindo que novos cargos sejam adicionados ao sistema dinamicamente, sem a necessidade de alterar o esquema do banco de dados.

#### 1.4. Modelo de Permissões (RBAC)
- **Decisão:** O modelo de permissões da aplicação de referência (baseado em campos JSON com listas de strings) será **descartado**.
- **Justificativa:** O modelo de RBAC já existente na implementação Python (com as tabelas `cargos`, `permissoes` e a tabela de junção `cargos_permissoes`) é relacionalmente mais correto, escalável e garante maior integridade dos dados. Continuaremos a utilizá-lo e expandi-lo conforme necessário.

### 2. Plano de Implementação Técnica (Passo a Passo)

O desenvolvimento seguirá as fases detalhadas abaixo. Ao final de cada fase, um commit será realizado.

#### **Fase 2.1: Atualização dos Modelos de Dados**
1.  **Ação:** Modificar `backend_python/models/models.py` para adicionar as classes `Familiar`, `Condecoracao`, `HistoricoCargo` e expandir a classe `MembroLoja`.
2.  **Ação:** Gerar um novo script de migração com o Alembic: `alembic revision --autogenerate -m "Implementa modelos detalhados de membros e entidades relacionadas"`.
3.  **Ação:** Aplicar a migração ao banco de dados: `alembic upgrade head`.
4.  **Checkpoint:** Realizar o commit com a mensagem `feat: Adiciona modelos de dados para membros, familiares, condecoracoes e historico`.

#### **Fase 2.2: Implementação dos Schemas (Contratos da API)**
1.  **Ação:** Criar os arquivos de schema Pydantic necessários (ex: `membro_schema.py`, `familiar_schema.py`) na pasta `schemas/`.
2.  **Ação:** Definir os schemas `Create`, `Update` e `Response` para cada nova entidade, garantindo a validação de dados na camada de API.
3.  **Checkpoint:** Realizar o commit com a mensagem `feat: Adiciona schemas Pydantic para gerenciamento de membros`.

#### **Fase 2.3: Implementação da Camada de Serviço (Lógica de Negócio)**
1.  **Ação:** Criar os arquivos de serviço (`membro_service.py`, etc.) na pasta `services/`.
2.  **Ação:** Implementar as funções de negócio (CRUD - Create, Read, Update, Delete) para cada entidade, incluindo validações e lógica de orquestração.
3.  **Checkpoint:** Realizar o commit com a mensagem `feat: Implementa logica de negocio para gerenciamento de membros`.

#### **Fase 2.4: Implementação da Camada de Controle (Endpoints da API)**
1.  **Ação:** Criar os arquivos de controller (`membro_controller.py`, etc.) na pasta `controllers/tenant/` (assumindo que estas são operações de tenant).
2.  **Ação:** Definir as rotas da API, injetando as dependências de serviço e autorização.
3.  **Ação:** Documentar cada endpoint com `summary`, `description` e `tags` para garantir uma documentação Swagger clara e completa.
4.  **Ação:** Adicionar os novos roteadores ao `main.py`.
5.  **Checkpoint:** Realizar o commit com a mensagem `feat: Expõe endpoints da API para gerenciamento de membros`.

#### **Fase 2.5: Finalização e Atualização da Documentação Principal**
1.  **Ação:** Revisar e testar o fluxo completo da nova funcionalidade.
2.  **Ação:** Mover as decisões de design desta seção para o `MANUAL_TECNICO.md`, criando novas seções conforme necessário.
3.  **Ação:** Limpar esta seção do `Concepcoes.md`, deixando-o pronto para a próxima funcionalidade.
4.  **Checkpoint:** Realizar o commit com a mensagem `docs: Atualiza manual tecnico com gerenciamento de membros`.
