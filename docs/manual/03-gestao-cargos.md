# Gestão de Cargos

Esta funcionalidade permite registrar e consultar o histórico de cargos ocupados pelos membros da Loja, bem como a diretoria atual.

## 4.1. Atribuição de Cargos

- **Regra:** Os cargos que um membro ocupa ou ocupou na Loja são registrados em seu histórico. O sistema foi desenhado para refletir a natureza periódica dos mandatos na Maçonaria. Um cargo pode ter uma data de início e uma data de término, representando um mandato concluído. Se a data de término for nula, o cargo é considerado o cargo atual do membro.

- **Implementação:** A atribuição de cargos é feita através do modelo `HistoricoCargo`, que associa um `MembroLoja` a um `Cargo` (previamente cadastrado na Loja) e especifica o período do mandato.

    - **Cadastro de Cargos:** O Webmaster primeiro cadastra os cargos disponíveis para a sua Loja (ex: Venerável Mestre, 1º Vigilante, Orador, Secretário). Essa lista é específica para cada Loja.
    - **Atribuição a Membros:** Em seguida, o Webmaster pode associar um membro a um cargo, definindo a `data_inicio` e, opcionalmente, a `data_termino`.

- **Consulta de Histórico:** A API permite consultar:
    - O histórico completo de cargos de um membro.
    - A diretoria da Loja para um determinado período (filtrando por `data_inicio` e `data_termino`).
    - O cargo atual de um membro (onde `data_termino` é nulo).

- **Obreiros:** Membros que não possuem um cargo ativo (sem registro em `HistoricoCargo` com `data_termino` nula) são considerados "Obreiros" do quadro.

- **Modelos de Dados:**
  - `Cargo` (tabela `cargos`): Armazena os cargos disponíveis para uma Loja.
    - `id_loja`: Chave estrangeira para a Loja.
    - `nome`: Nome do cargo.
    - `descricao`: Descrição das atribuições.
  - `HistoricoCargo` (tabela `historico_cargos`):
    - `id_membro`: Chave estrangeira para o `MembroLoja`.
    - `id_cargo`: Chave estrangeira para o `Cargo`.
    - `data_inicio`: Data de início do mandato.
    - `data_termino`: Data de término do mandato (pode ser nula).
