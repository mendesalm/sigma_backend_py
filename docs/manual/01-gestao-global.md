# Gestão Global (Nível Super Administrador)

Estas funcionalidades são acessíveis apenas por Super Administradores e são a base para a configuração de todo o sistema SiGMa.

## 2.1. Criação de Super Administrador

- **Regra:** Um Super Administrador é o nível mais alto de usuário, com acesso irrestrito às configurações globais do sistema. Suas responsabilidades incluem a criação de tenants (Lojas), a gestão de outros Super Administradores e a configuração de parâmetros globais.

- **Implementação:** A criação do primeiro Super Administrador é um passo fundamental na instalação do sistema e é realizada através de um processo de *seeding* do banco de dados ou por meio de um script de setup inicial. Contas subsequentes de Super Administradores são gerenciadas através de endpoints de API específicos, que exigem autenticação de um Super Administrador já existente.

- **Modelo de Dados:** `SuperAdministrador` (tabela `super_administradores`)
  - `id`: Identificador único.
  - `nome`: Nome do administrador.
  - `email`: Email para login (deve ser único).
  - `senha_hash`: Hash da senha.

## 2.2. Cadastro de Potências e Lojas (Tenants)

- **Regra:** O sistema permite o cadastro de Lojas, que funcionam como "tenants" individuais e isolados. Uma Loja pode representar uma Potência, um Grande Oriente ou uma Loja Simbólica. A hierarquia entre elas (ex: Lojas jurisdicionadas a um Grande Oriente) é gerenciada através de uma tabela de relacionamento (`hierarquia_lojas`), permitindo a construção de estruturas organizacionais complexas.

- **Implementação:** Super Administradores podem cadastrar novas Lojas através de um endpoint da API. Ao cadastrar uma Loja, são definidos parâmetros essenciais:
  - **Nome e Número:** Identificadores da Loja.
  - **Domínio:** Um subdomínio ou identificador único para o tenant (ex: `loja-acacia-1`).
  - **Plano e Limites:** Definição do plano de assinatura e limites de uso (ex: número máximo de membros).
  - **Responsável Técnico:** O contato principal para a gestão da Loja.

- **Modelos de Dados:**
  - `Loja` (tabela `lojas`): Armazena os detalhes de cada tenant.
  - `HierarquiaLoja` (tabela `hierarquia_lojas`): Mapeia o relacionamento entre Lojas (ex: `id_loja_pai` e `id_loja_filha`).

## 2.3. Geração de Webmaster

- **Regra:** Para cada Loja (tenant) criada, um usuário `Webmaster` é gerado automaticamente. Este usuário possui as permissões administrativas para gerenciar aquela Loja específica, incluindo o cadastro de membros, a gestão de cargos e o agendamento de sessões.

- **Implementação:** A criação do Webmaster está diretamente atrelada à criação da Loja. O mesmo endpoint de API que cria a Loja também é responsável por gerar a conta de Webmaster associada, garantindo que cada tenant tenha seu administrador inicial. As credenciais do Webmaster são então enviadas de forma segura para o responsável técnico da Loja.

- **Modelo de Dados:** `Webmaster` (tabela `webmasters`)
  - `id`: Identificador único.
  - `id_loja`: Chave estrangeira para a Loja que ele administra.
  - `nome`: Nome do Webmaster.
  - `email`: Email para login.
  - `senha_hash`: Hash da senha.
