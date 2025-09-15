# Manual do Sigma

Este manual descreve em detalhes a aplicação Sigma, suas funcionalidades, regras de negócio e estrutura.

## 1. Visão Geral

O Sigma é um sistema de gerenciamento para lojas maçônicas, projetado para otimizar a administração, comunicação e manutenção de registros.

## 2. Modelos de Dados

A seguir, a descrição detalhada dos modelos de dados da aplicação.

### 2.1. MembroLoja

O modelo `MembroLoja` representa um membro de uma loja maçônica. A tabela `membros_loja` armazena informações detalhadas sobre cada membro, incluindo dados pessoais, de contato, maçônicos e de autenticação.

#### Campos:

*   **id**: Identificador único do membro.
*   **id_loja**: Chave estrangeira para a loja à qual o membro pertence.
*   **email**: Email do membro, usado para login e comunicação.
*   **senha_hash**: Hash da senha do membro.
*   **email_verification_token**: Token para verificação de email.
*   **email_verification_expires**: Data de expiração do token de verificação de email.
*   **reset_password_token**: Token para reset de senha.
*   **reset_password_expires**: Data de expiração do token de reset de senha.
*   **ultimo_login**: Data do último login do membro.
*   **nome_completo**: Nome completo do membro.
*   **cpf**: CPF do membro.
*   **cim**: Carteira de Identidade Maçônica.
*   **identidade**: Documento de identidade do membro.
*   **foto_pessoal_caminho**: Caminho para a foto do membro.
*   **data_nascimento**: Data de nascimento do membro.
*   **data_casamento**: Data de casamento do membro.
*   **naturalidade**: Cidade de nascimento do membro.
*   **nacionalidade**: País de nascimento do membro.
*   **religiao**: Religião do membro.
*   **nome_pai**: Nome do pai do membro.
*   **nome_mae**: Nome da mãe do membro.
*   **formacao_academica**: Formação acadêmica do membro.
*   **ocupacao**: Ocupação profissional do membro.
*   **local_trabalho**: Local de trabalho do membro.
*   **telefone**: Telefone de contato do membro.
*   **endereco_rua**: Rua do endereço do membro.
*   **endereco_numero**: Número do endereço do membro.
*   **endereco_bairro**: Bairro do endereço do membro.
*   **endereco_cidade**: Cidade do endereço do membro.
*   **endereco_cep**: CEP do endereço do membro.
*   **situacao**: Situação do membro na loja (Ativo, Inativo, etc.).
*   **graduacao**: Grau maçônico do membro (Aprendiz, Companheiro, Mestre, Mestre Instalado).
*   **grau_filosofico**: Grau filosófico do membro.
*   **data_iniciacao**: Data de iniciação do membro.
*   **data_elevacao**: Data de elevação do membro.
*   **data_exaltacao**: Data de exaltação do membro.
*   **data_filiacao**: Data de filiação do membro.
*   **data_regularizacao**: Data de regularização do membro.
*   **status_cadastro**: Status do cadastro do membro (Pendente, Aprovado, Rejeitado, VerificacaoEmailPendente).

### 2.2. Familiar

O modelo `Familiar` representa um familiar de um membro da loja.

#### Campos:

*   **id**: Identificador único do familiar.
*   **id_membro**: Chave estrangeira para o membro ao qual o familiar está associado.
*   **nome_completo**: Nome completo do familiar.
*   **parentesco**: Grau de parentesco com o membro (Cônjuge, Filho, Filha).
*   **data_nascimento**: Data de nascimento do familiar.
*   **email**: Email de contato do familiar.
*   **telefone**: Telefone de contato do familiar.
*   **falecido**: Indica se o familiar é falecido.

### 2.3. SessaoMaconica

O modelo `SessaoMaconica` representa uma sessão maçônica.

#### Campos:

*   **id**: Identificador único da sessão.
*   **id_loja**: Chave estrangeira para a loja que está realizando a sessão.
*   **data_sessao**: Data e hora da sessão.
*   **tipo**: Tipo da sessão (Ordinária, Magna, Extraordinária).
*   **subtipo**: Subtipo da sessão.
*   **status**: Status da sessão (Agendada, Em Andamento, Realizada, Cancelada).

### 2.4. PresencaSessao

O modelo `PresencaSessao` registra a presença de um membro da loja em uma sessão.

#### Campos:

*   **id**: Identificador único do registro de presença.
*   **id_sessao**: Chave estrangeira para a sessão.
*   **id_membro**: Chave estrangeira para o membro (anulável).
*   **id_visitante**: Chave estrangeira para o visitante (anulável).
*   **status_presenca**: Status da presença (Presente, Justificado, Ausente).
*   **data_hora_checkin**: Data e hora do check-in.

### 2.5. LojaExterna

O modelo `LojaExterna` representa uma loja maçônica que não é cliente do sistema Sigma.

#### Campos:

*   **id**: Identificador único da loja externa.
*   **nome**: Nome da loja externa.
*   **numero**: Número da loja externa.
*   **obediencia**: Obediência da loja externa.
*   **cidade**: Cidade da loja externa.
*   **pais**: País da loja externa.

### 2.6. Visitante

O modelo `Visitante` representa um visitante.

#### Campos:

*   **id**: Identificador único do visitante.
*   **nome_completo**: Nome completo do visitante.
*   **email**: Email do visitante.
*   **telefone**: Telefone do visitante.
*   **cim**: CIM do visitante.
*   **id_loja_externa**: Chave estrangeira para a loja externa do visitante.

## 3. Lógica de Agendamento e Status

### 3.1. Sugestão de Data

Um endpoint `GET /api/tenant/sessoes/suggest-next-date/{loja_id}` foi criado para sugerir a data da próxima sessão com base na periodicidade da loja e na data da última sessão. A criação efetiva da sessão permanece manual.

### 3.2. Atualização de Status

Um endpoint `PUT /api/tenant/sessoes/{sessao_id}/status` foi implementado para permitir a atualização manual do status de uma sessão (Agendada, Em Andamento, Realizada, Cancelada).

## 4. Lógica de Registro de Presença

O sistema agora suporta dois fluxos distintos para registro de presença:

### 4.1. Fluxo A (Manual)

Um usuário com permissão adequada pode adicionar/remover registros de presença de membros e visitantes através dos seguintes endpoints:

*   `PUT /api/tenant/sessoes/{sessao_id}/attendance`: Atualiza o status de presença de membros e visitantes.
*   `POST /api/tenant/sessoes/{sessao_id}/visitors`: Adiciona um novo visitante e registra sua presença na sessão.
*   `DELETE /api/tenant/sessoes/visitors/{visitor_id}`: Remove um visitante e seu registro de presença.

### 4.2. Fluxo B (Check-in por App)

Um endpoint público `POST /api/checkin` foi criado para ser consumido por um futuro aplicativo móvel. Este endpoint:

*   Recebe a identidade do usuário (via JWT do app) e o ID da loja (via QR Code).
*   Valida a janela de tempo para registro de presença (2 horas antes e 2 horas depois do início da sessão) através do middleware `check_attendance_window`.
*   Registra a presença do membro na sessão.

## 5. Geração de QR Code

Um endpoint `GET /api/global/tenants/{loja_id}/qr-code` foi implementado para gerar um QR Code para uma loja específica. O QR Code contém informações essenciais da loja para identificação pelo aplicativo móvel.