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