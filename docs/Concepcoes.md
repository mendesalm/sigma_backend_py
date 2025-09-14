# Documento de Concepção: Funcionalidades em Desenvolvimento

Este documento serve como um registro vivo do planejamento e das decisões de design para as funcionalidades que estão sendo implementadas. Uma vez que uma funcionalidade é concluída, sua documentação é movida daqui para o `MANUAL_TECNICO.md`.

---

## **Em Andamento: Gerenciamento de Sessões Maçônicas**

**Objetivo:** Implementar um sistema completo para agendamento, gerenciamento e registro histórico de sessões maçônicas, incluindo o registro de presença de membros e visitantes.

### 1. Análise e Decisões de Design

Com base nos requisitos, as seguintes decisões de design foram tomadas:

#### 1.1. Modelos de Dados

Serão introduzidos os seguintes novos modelos no arquivo `models/models.py`:

- **`SessaoMaconica`**: A entidade central desta funcionalidade.
    - **Campos:** `id_loja` (FK para `lojas`), `data_hora_inicio`, `status` (ENUM: `Agendada`, `Em Andamento`, `Realizada`, `Cancelada`), `tipo` (ENUM: `Ordinária`, `Magna`, `Extraordinária`), `subtipo` (String, para acomodar a variedade de subtipos).

- **`LojaExterna`**: Tabela para armazenar lojas não-clientes do sistema, cujos membros podem visitar sessões (`banco_de_lojas`).
    - **Campos:** `nome_loja`, `obediencia`, `cidade`, `pais`.

- **`Visitante`**: Tabela para o cadastro de maçons de lojas não-clientes (`banco_de_visitantes`).
    - **Campos:** `nome_completo`, `email`, `cim`, `id_loja_externa` (FK para `lojas_externas`).

- **`PresencaSessao`**: Tabela de associação para registrar a presença em uma sessão.
    - **Campos:** `id_sessao` (FK para `sessoes_maconicas`), `id_membro` (FK para `membros_loja`, anulável), `id_visitante` (FK para `visitantes`, anulável), `data_hora_checkin`.

#### 1.2. Lógica de Agendamento e Status

- **Sugestão de Data:** Será criado um endpoint (`GET /api/tenant/sessoes/sugerir-proxima`) que usará os campos `periodicidade` e `dia_sessoes` da tabela `lojas`, em conjunto com a data da última sessão registrada, para sugerir a data da próxima sessão. A criação efetiva será manual.
- **Atualização de Status:** A atualização do status da sessão (de `Agendada` para `Em Andamento`, etc.) será, inicialmente, uma ação manual realizada através de um endpoint da API (`PUT /api/tenant/sessoes/{id}/status`).
    - **Nota Arquitetural:** A automação por tarefas agendadas (scheduler) é uma melhoria futura e não será implementada neste ciclo para manter o escopo gerenciável.

#### 1.3. Lógica de Registro de Presença

O sistema suportará dois fluxos distintos:

- **Fluxo A (Manual):** Um usuário com a permissão `sessao:gerenciar_presenca` (ex: Chanceler) poderá adicionar/remover registros de presença de membros e visitantes através de endpoints específicos.
- **Fluxo B (Check-in por App):** Será criado um endpoint público (`POST /api/checkin`) para ser consumido por um futuro aplicativo móvel. Este endpoint receberá a identidade do usuário (via JWT do app) e o ID da loja (via QR Code), validará a janela de tempo (2h antes/depois do início da sessão) e registrará a presença.

#### 1.4. Permissões (RBAC)

Serão criadas novas ações na tabela `permissoes` para controlar o acesso a esta funcionalidade. Exemplos:
- `sessao:criar`: Permite agendar novas sessões.
- `sessao:gerenciar`: Permite editar, cancelar ou deletar sessões.
- `sessao:gerenciar_presenca`: Permite manipular a lista de presença manualmente.

### 2. Plano de Implementação Técnica (Passo a Passo)

O desenvolvimento seguirá as fases detalhadas abaixo:

#### **Fase 3.1: Modelos de Dados e Migração**
1.  **Ação:** Adicionar as classes `SessaoMaconica`, `LojaExterna`, `Visitante` e `PresencaSessao` ao `models/models.py`.
2.  **Ação:** Gerar um novo script de migração com Alembic: `alembic revision --autogenerate -m "Adiciona modelos para gestao de sessoes maconicas"`.
3.  **Ação:** Aplicar a migração ao banco de dados: `alembic upgrade head`.
4.  **Checkpoint:** Commit com a mensagem `feat: Adiciona modelos de dados para sessoes maconicas`.

#### **Fase 3.2: Schemas, Serviços e Endpoints (CRUD Básico)**
1.  **Ação:** Criar os schemas Pydantic, serviços e controllers para o CRUD básico de `SessaoMaconica`.
2.  **Ação:** Implementar o endpoint de sugestão de data (`GET /sugerir-proxima`).
3.  **Ação:** Implementar o endpoint de atualização de status (`PUT /{id}/status`).
4.  **Checkpoint:** Commit com a mensagem `feat: Implementa CRUD basico e logica de agendamento de sessoes`.

#### **Fase 3.3: Implementação do Cadastro de Visitantes**
1.  **Ação:** Criar schemas, serviços e controllers para o CRUD de `LojaExterna` e `Visitante`.
2.  **Checkpoint:** Commit com a mensagem `feat: Implementa cadastro de visitantes e lojas externas`.

#### **Fase 3.4: Implementação do Registro de Presença**
1.  **Ação:** Implementar os endpoints para o registro manual de presença (Fluxo A).
2.  **Ação:** Implementar o endpoint e a lógica para o check-in via QR Code (Fluxo B).
3.  **Checkpoint:** Commit com a mensagem `feat: Implementa logica e endpoints para registro de presenca`.

#### **Fase 3.5: Finalização e Documentação**
1.  **Ação:** Revisar toda a funcionalidade e adicionar as novas permissões ao sistema.
2.  **Ação:** # Documento de Concepção: Funcionalidades em Desenvolvimento

Este documento serve como um registro vivo do planejamento e das decisões de design para as funcionalidades que estão sendo implementadas. Uma vez que uma funcionalidade é concluída, sua documentação é movida daqui para o `MANUAL_TECNICO.md`.

---

## Próxima Funcionalidade: (A ser definido)

3.  **Ação:** Limpar esta seção do `Concepcoes.md`.
4.  **Checkpoint:** Commit com a mensagem `docs: Atualiza manual tecnico com gestao de sessoes`.