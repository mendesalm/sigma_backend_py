# Gerenciamento de Sessões Maçônicas

Esta funcionalidade permite o agendamento, controle de presença e registro histórico das sessões maçônicas da Loja.

## 5.1. Agendamento de Sessão

- **Regra:** Uma sessão é criada para uma Loja em uma data e hora específicas. Ela possui um `tipo` (Ordinária, Magna, Extraordinária, etc.) e um `status` (Agendada, Em Andamento, Realizada, Cancelada). O sistema também pode sugerir a data da próxima sessão com base na periodicidade configurada para a Loja (ex: semanal, quinzenal).

- **Implementação:** Um usuário com a permissão `sessao:criar` pode agendar novas sessões. A API oferece um endpoint para criar a sessão e outro para sugerir a data da próxima, facilitando o planejamento.

- **Modelo de Dados:** `SessaoMaconica` (tabela `sessoes_maconicas`)
  - `id_loja`: Chave estrangeira para a Loja.
  - `data_sessao`: Data e hora da sessão.
  - `tipo_sessao`: Tipo da sessão.
  - `status_sessao`: Status atual da sessão.

## 5.2. Registro de Presença

- **Regra:** A presença em uma sessão pode ser registrada para membros do quadro da Loja e para visitantes de outras Lojas. O sistema diferencia entre os dois para manter um registro preciso.

- **Implementação:**
    - **Membros da Loja:** A presença é registrada na tabela `PresencaSessao`, vinculando o `id_membro` ao `id_sessao`. Isso é feito através de uma interface onde o responsável pela lista de presença pode marcar os membros presentes.
    - **Visitantes:** Para registrar um visitante, ele deve primeiro ser cadastrado no sistema. 
        1.  Se a Loja de origem do visitante não for cliente do SiGMa, ela é primeiro registrada como uma `LojaExterna`.
        2.  Em seguida, o `Visitante` é criado e associado a essa `LojaExterna`.
        3.  Finalmente, a presença é registrada na tabela `PresencaSessao`, vinculando o `id_visitante` ao `id_sessao`.

- **Modelos de Dados:**
  - `PresencaSessao` (tabela `presencas_sessao`): Tabela de junção que registra a presença.
    - `id_sessao`: Chave estrangeira para a sessão.
    - `id_membro`: Chave estrangeora para o membro da Loja (pode ser nulo).
    - `id_visitante`: Chave estrangeira para o visitante (pode ser nulo).
  - `Visitante` (tabela `visitantes`): Armazena os dados de visitantes.
  - `LojaExterna` (tabela `lojas_externas`): Armazena informações sobre Lojas que não são tenants no sistema.
