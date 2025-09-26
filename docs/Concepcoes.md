# Documento de Concepção: Funcionalidades em Desenvolvimento

Este documento serve como um registro vivo do planejamento e das decisões de design para as funcionalidades que estão sendo implementadas. Uma vez que uma funcionalidade é concluída, sua documentação é movida daqui para o `MANUAL_TECNICO.md`.

---

## Refatoração do Frontend para Backend Python e Nova Estilização

**Objetivo:** Adaptar o frontend existente para consumir a API do `backend_python` e integrar um novo padrão de estilização.

### Resumo do Trabalho Realizado:

Uma refatoração extensiva foi realizada nas principais páginas do frontend para garantir a comunicação correta com o novo backend Python. As seguintes melhorias foram implementadas:

1.  **Centralização da Comunicação API:** Foi criada uma instância centralizada do `axios` (`apiClient`) em `frontend/src/api/axiosConfig.ts`. Esta instância é responsável por:
    *   Definir a URL base da API (`http://localhost:8000`).
    *   Incluir automaticamente o token de autenticação (JWT) em todas as requisições, obtido do `localStorage`.
    *   Simplificar as chamadas de API em todo o frontend.

2.  **Contexto de Autenticação Unificado:** O contexto de autenticação (`frontend/src/contexto/ContextoAutenticacao.tsx`) foi padronizado e utilizado em todas as páginas relevantes para gerenciar o estado de autenticação do usuário (`token`, `usuario`, `perfil`).

3.  **Integração de Nova Estilização:** Um novo padrão de design, baseado em variáveis CSS, foi integrado ao projeto. Isso incluiu:
    *   Atualização do `frontend/src/index.css` com variáveis CSS para cores, tipografia e layout, suportando temas claro e escuro.
    *   Modificação do `frontend/src/theme.ts` para criar um tema Material-UI (`sigmaTheme`) que consome essas variáveis CSS, garantindo que os componentes Material-UI sigam o novo design.
    *   Aplicação do `ThemeProvider` e `CssBaseline` em `frontend/src/App.tsx` para garantir a consistência visual em toda a aplicação.

4.  **Páginas Refatoradas:** As seguintes páginas foram completamente refatoradas para consumir a nova API e aplicar a nova estilização:
    *   `Login.tsx` (Login de Super Admin)
    *   `LojasPage.tsx` (Gerenciamento Global de Lojas)
    *   `CargosPage.tsx` (Gerenciamento Global de Cargos)
    *   `PermissoesPage.tsx` (Gerenciamento Global de Permissões)
    *   `CargosPermissoesPage.tsx` (Associação Global Cargo-Permissão)
    *   `ClassesLojasPage.tsx` (Gerenciamento Global de Classes de Loja)
    *   `DashboardPage.tsx` (Dashboard de Super Admin Global)
    *   `RegistroMembroPage.tsx` (Registro de Membros por Tenant)
    *   `AtribuicaoCargosWebmasterPage.tsx` (Atribuição de Cargos para Membros por Tenant)
    *   `ProcessosAdministrativosPage.tsx` (Processos Administrativos por Tenant)

### Limitações Identificadas e Propostas de Solução:

Durante a refatoração, algumas limitações na comunicação entre frontend e backend foram identificadas, principalmente relacionadas à atribuição de cargos:

1.  **Atribuição Inicial de Cargos:**
    *   **Limitação:** O endpoint `POST /webmaster/atribuicao-cargos/assign` do backend espera o ID de uma associação de membro-cargo existente (`lodge_member_association_id`) para atualizar um cargo. Ele não permite a criação da *primeira* associação de cargo para um membro que ainda não possui nenhum cargo registrado.
    *   **Solução Proposta (Backend):** Recomenda-se a criação de um novo endpoint no backend, por exemplo, `POST /webmaster/atribuicao-cargos/atribuir-primeiro-cargo`, que aceite o `id_membro` e o `id_cargo` e crie a primeira entrada no histórico de cargos para o membro. Alternativamente, o endpoint `assign` poderia ser modificado para lidar com ambos os cenários.

2.  **Consulta de Diretorias por Período:**
    *   **Limitação:** Atualmente, não há um endpoint dedicado no backend para consultar a composição de diretorias por um período específico.
    *   **Solução Proposta (Backend):** Recomenda-se a criação de um novo endpoint, por exemplo, `GET /api/tenant/diretorias`, que aceite `data_inicio` e `data_fim` como parâmetros e retorne os membros que ocuparam cargos nesse período. Este endpoint faria a lógica de consulta no `HistoricoCargo` e agregaria as informações necessárias.

---

## Próxima Funcionalidade: (A ser definido)

Com a refatoração do frontend concluída e as principais funcionalidades adaptadas, o sistema está pronto para novas implementações ou refinamentos.