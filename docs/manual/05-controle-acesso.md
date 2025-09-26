# Controle de Acesso (RBAC)

O SiGMa utiliza um sistema de Controle de Acesso Baseado em Cargos (RBAC - Role-Based Access Control) para gerenciar o que cada usuário pode fazer dentro do sistema. As permissões são associadas a cargos, e os usuários herdam as permissões do cargo que ocupam.

## 6.1. Permissões (RBAC)

- **Regra:** O acesso às funcionalidades do sistema é controlado por um conjunto de permissões. Um cargo (como "Venerável Mestre" ou "Secretário") pode ter múltiplas permissões, e um membro que ocupa esse cargo herda automaticamente essas permissões. Isso permite uma gestão de acesso granular e flexível.

- **Implementação:**
    - **Permissões:** As permissões são definidas no sistema e representam ações específicas (ex: `sessao:criar`, `membro:editar`).
    - **Cargos:** Os cargos são criados pelo Webmaster da Loja.
    - **Associação:** O Webmaster associa as permissões aos cargos. Por exemplo, o cargo de "Secretário" pode ter as permissões `sessao:criar` e `sessao:gerenciar_presenca`.
    - **Herança:** Quando um membro é atribuído a um cargo através do `HistoricoCargo` (com `data_termino` nula), ele passa a ter as permissões daquele cargo.

- **Exemplo de Permissões para Sessões:**
    - `sessao:criar`: Permite agendar novas sessões.
    - `sessao:gerenciar`: Permite editar, cancelar ou deletar sessões agendadas.
    - `sessao:gerenciar_presenca`: Permite adicionar ou remover manualmente a presença de membros e visitantes em uma sessão.

- **Modelos de Dados:**
  - `Permissao` (tabela `permissoes`): Armazena todas as permissões disponíveis no sistema.
  - `CargoPermissao` (tabela `cargo_permissoes`): Tabela de junção que associa `Cargo` a `Permissao`.
