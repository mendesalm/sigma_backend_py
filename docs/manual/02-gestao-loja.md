# Gestão da Loja (Nível Tenant / Webmaster)

Estas funcionalidades são gerenciadas pelo Webmaster de cada Loja para seus próprios membros e dados. O acesso é restrito ao tenant (Loja) ao qual o Webmaster pertence.

## 3.1. Cadastro e Gestão de Membros

- **Regra:** O Webmaster pode cadastrar e gerenciar os membros de sua Loja. Um membro pode ser um usuário com acesso ao sistema (com email e senha para login) ou apenas um registro no quadro da Loja (sem credenciais de acesso). Isso permite manter um registro completo de todos os obreiros, mesmo aqueles que não utilizarão a plataforma digitalmente.

- **Implementação:** O cadastro é realizado através de um formulário completo na API, que abrange diversas seções de informações do membro:

    - **Dados Pessoais:** `nome_completo`, `cpf`, `identidade`, `data_nascimento`, `data_casamento`, `naturalidade`, `nacionalidade`, `religiao`, `nome_pai`, `nome_mae`.
    - **Contato:** `telefone`, `endereco_rua`, `endereco_numero`, `endereco_bairro`, `endereco_cidade`, `endereco_cep`.
    - **Formação e Ocupação:** `formacao_academica`, `ocupacao`, `local_trabalho`.
    - **Dados Maçônicos:** `cim` (Cadastro de Identificação Maçônica), `graduacao` (Aprendiz, Companheiro, Mestre), `grau_filosofico`, `data_iniciacao`, `data_elevacao`, `data_exaltacao`, `data_filiacao`, `data_regularizacao`.
    - **Status:**
        - `situacao`: Controla o status do membro na Loja (Ativo, Inativo, Licenciado, etc.).
        - `status_cadastro`: Define o estado do registro no sistema (Pendente, Aprovado, Rejeitado).
    - **Foto Pessoal:** Um endpoint de upload permite o envio da foto do membro. O caminho para o arquivo (`foto_pessoal_caminho`) é armazenado no banco de dados.

- **Modelo de Dados:** `MembroLoja` (tabela `membros_loja`)

## 3.2. Gestão de Familiares

- **Regra:** O sistema permite registrar os familiares de um membro, como Cônjuge, Filho(a), para fins de cadastro e contato. Isso é útil para a organização de eventos sociais e para o Clube das Acácias.

- **Implementação:** Associado a um registro de `MembroLoja`, é possível criar múltiplos registros de `Familiar`. Cada registro inclui:
    - `nome_completo`
    - `parentesco` (Cônjuge, Filho, Filha)
    - `data_nascimento`
    - `email`
    - `telefone`
    - `falecido` (booleano)

- **Modelo de Dados:** `Familiar` (tabela `familiares`)

## 3.3. Gestão de Condecorações

- **Regra:** As condecorações, títulos e honrarias recebidas por um membro ao longo de sua jornada maçônica podem ser registradas em seu perfil.

- **Implementação:** Para cada `MembroLoja`, é possível adicionar registros de condecorações, especificando:
    - `titulo`: O nome da condecoração (ex: "Benemérito da Ordem").
    - `data_recebimento`: A data em que a honraria foi concedida.
    - `observacoes`: Detalhes adicionais sobre a condecoração.

- **Modelo de Dados:** `Condecoracao` (tabela `condecoracoes`)
