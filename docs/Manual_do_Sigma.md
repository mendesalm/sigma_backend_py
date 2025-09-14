# Manual do SiGMa: Regras de Negócio e Funcionalidades

Este manual detalha as regras de negócio e as funcionalidades do Sistema Integrado de Gestão de Lojas Maçônicas (SiGMa). Ele serve como a fonte definitiva para o entendimento do comportamento da aplicação, descrevendo suas capacidades em profundidade, independentemente da implementação técnica.

---

## 1. Visão Geral do Sistema SiGMa

O SiGMa é uma plataforma projetada para auxiliar na gestão de Lojas Maçônicas, oferecendo ferramentas para o gerenciamento de membros, sessões, finanças, patrimônio e outras atividades administrativas e rituais. O sistema opera em um modelo multi-tenant, onde cada Loja é um tenant isolado, mas com a possibilidade de relações hierárquicas entre elas (Potências Federal, Estadual e Lojas).

## 2. Gerenciamento de Lojas e Entidades (Global)

Esta funcionalidade abrange a administração das entidades fundamentais do sistema: as Lojas (que podem ser Potências Federal, Estadual ou Lojas Simbólicas) e seus administradores de alto nível.

### 2.1. Atores Principais

-   **SuperAdministrador:** O usuário de mais alto nível no sistema. Possui acesso irrestrito a todas as funcionalidades e dados de todas as Lojas e Entidades. É responsável pela criação e gerenciamento de outras instâncias de SuperAdministradores, bem como pelo onboarding de novas Lojas.
-   **Webmaster:** O administrador de uma Loja específica. Esta conta é criada automaticamente no momento do onboarding da Loja e é responsável pela configuração inicial da Loja e pelo cadastro de seus membros.

### 2.2. Regras de Negócio Chave

-   **Hierarquia de Entidades:** O sistema suporta uma hierarquia de Lojas, permitindo a modelagem de relações como Potência Federal > Potências Estaduais > Lojas Simbólicas. Esta hierarquia é utilizada para relatórios e controle de acesso.
-   **Onboarding de Lojas:** O processo de criação de uma nova Loja é uma operação atômica realizada exclusivamente por um SuperAdministrador. Este processo inclui:
    -   Criação do registro da Loja.
    -   Geração e associação de uma conta de Webmaster para a Loja.
    -   Definição da posição da Loja na hierarquia existente.
-   **Acesso Global:** As funcionalidades de gerenciamento de Lojas e Entidades são acessíveis apenas por SuperAdministradores.

## 3. Gerenciamento de Membros

Esta funcionalidade permite o cadastro e a gestão detalhada dos membros de cada Loja, incluindo seus dados pessoais, maçônicos, familiares, condecorações e histórico de cargos.

### 3.1. Atores Principais

-   **Webmaster:** Responsável por cadastrar e gerenciar os membros de sua Loja.
-   **Membro da Loja:** Usuário que pode consultar seus próprios dados e, dependendo de suas permissões, acessar informações de outros membros ou funcionalidades específicas.

### 3.2. Regras de Negócio Chave

-   **Cadastro Detalhado de Membros:** Cada membro possui um registro abrangente que inclui:
    -   **Dados Pessoais:** Nome completo, CPF, CIM (Carteira de Identidade Maçônica), data de nascimento, naturalidade, nacionalidade, e-mail, telefone, endereço.
    -   **Dados Maçônicos:** Situação (Ativo, Inativo, etc.), Grau (Aprendiz, Companheiro, Mestre, Mestre Instalado), data de iniciação.
    -   **Autenticação:** Membros podem ter credenciais de login (e-mail e senha) para acessar o sistema.
-   **Gerenciamento de Familiares:** É possível registrar e gerenciar os familiares de cada membro, especificando o parentesco (cônjuge, filho, filha) e dados básicos como nome e data de nascimento.
-   **Registro de Condecorações:** O sistema permite registrar as condecorações e honrarias recebidas por cada membro, incluindo o título, a data de recebimento e observações.
-   **Histórico de Cargos:** É mantido um histórico dos cargos que cada membro ocupou dentro da Loja, registrando o cargo, a data de início e a data de término.
-   **Controle de Acesso:** O acesso às funcionalidades de gerenciamento de membros é restrito a usuários autenticados e autorizados (ex: Webmaster da Loja, ou membros com permissões específicas).

## 4. Gerenciamento de Sessões Maçônicas

Esta funcionalidade permite o agendamento, gerenciamento e registro histórico das sessões maçônicas, incluindo a definição de tipos, subtipos, status e o registro de presença de membros e visitantes.

### 4.1. Atores Principais

-   **Diretoria da Loja (ex: Secretário, Chanceler):** Responsáveis pela criação, edição, cancelamento e deleção de sessões, bem como pelo gerenciamento manual da lista de presença.
-   **Membros da Loja:** Podem consultar a agenda de sessões e registrar sua própria presença.
-   **Visitantes:** Maçons de outras Lojas (clientes ou não do SiGMa) que podem registrar sua presença em sessões.

### 4.2. Regras de Negócio Chave

-   **Tipos e Subtipos de Sessão:** As sessões são categorizadas por `Tipo` (Ordinária, Magna, Extraordinária) e `Subtipo` (uma lista detalhada de subtipos específicos para cada tipo, como Iniciação, Elevação, Banquete Ritualístico, etc.).
-   **Ciclo de Vida (Status da Sessão):** Uma sessão progride através dos status: `Agendada` -> `Em Andamento` -> `Realizada`. Também pode ser `Cancelada`. O status pode ser atualizado manualmente pela diretoria.
-   **Agendamento da Sessão:**
    -   As Lojas possuem uma periodicidade definida (semanal, quinzenal, mensal), dia da semana e hora para suas sessões.
    -   O sistema pode **sugerir** a próxima data e hora da sessão com base nesses dados e no histórico de sessões, facilitando o planejamento.
-   **Registro de Presença:**
    -   **Manual (Fluxo A):** Um usuário com permissão específica (ex: Chanceler) pode registrar, ler, atualizar e deletar registros de presença para uma sessão diretamente no sistema, a qualquer tempo após o início da sessão.
    -   **Automático via Aplicativo Móvel (Fluxo B):**
        -   **Membros Intrínsecos:** Membros de Lojas clientes do SiGMa fazem login com CIM e senha no aplicativo móvel. O aplicativo lê um QR Code da Loja anfitriã. O sistema verifica o ID da Loja do usuário e registra a presença na sessão agendada dentro de uma janela temporal (2 horas antes a 2 horas após o início da sessão).
        -   **Membros Extrínsecos (Visitantes):** Maçons de Lojas não-clientes do SiGMa devem realizar um cadastro prévio no sistema via aplicativo. Eles também usam o aplicativo para ler o QR Code da Loja anfitriã e registrar sua presença na sessão dentro da janela temporal.
-   **Cadastro de Lojas Externas e Visitantes:** O sistema permite o cadastro de Lojas Externas (não clientes do SiGMa) e de Visitantes (maçons de Lojas Externas) para fins de registro de presença em sessões.

## 5. Próximas Funcionalidades (A Serem Detalhadas)

Esta seção será expandida à medida que novas funcionalidades forem planejadas e implementadas.
