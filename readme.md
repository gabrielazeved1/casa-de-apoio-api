# API e Dashboard - Gestão de Casa de Apoio (Teste Técnico)

Bem-vindo ao repositório de revitalização do sistema de Gestão de Usuários para Casas de Apoio. Este projeto é uma API RESTful em Django com a missão de registrar check-ins, check-outs e consumo de serviços por pacientes com câncer e seus acompanhantes, fornecendo dados estruturados para a prestação de contas.

## O que foi feito neste desafio?

1. **Migração Local:** Remoção de dependências de deploy (Heroku) e configuração de banco de dados SQLite3 para desenvolvimento rápido.
2. **Modernização Core:** Atualização de todas as bibliotecas para as versões mais recentes e seguras do mercado (Django 6.0.3, DRF 3.17.1).
3. **Documentação Swagger:** Implementação do `drf-spectacular` gerando rotas interativas para o front-end.
4. **Dashboard Executivo:** Criação de um painel MVC em tempo real com Chart.js, acessível publicamente, detalhando ocupação e consumo.
5. **Regras de Negócio e Qualidade de Dados:** Implementação de 4 melhorias cruciais detalhadas abaixo.

---

## Melhorias Implementadas (Regras de Negócio)

### Melhoria 1: Bloqueio de múltiplos Check-ins ativos para a mesma pessoa

- **User Story:** Como recepcionista, eu quero que o sistema me impeça de fazer um novo check-in para um paciente que já está na casa, para evitar dados duplicados e furos na contagem de leitos.
- **5W2H:**
  - **Who (Quem):** Recepcionista / Sistema.
  - **What (O Que):** Bloquear a criação de um Check-in se a pessoa já possuir um Check-in com `active=True`.
  - **When (Quando):** No momento de validação e salvamento de um novo Check-in.
  - **Where (Onde):** No Model de `Checkin` (método `clean`).
  - **Why (Por Que):** Evitar inconsistência na ocupação da casa e relatórios adulterados.
  - **How (Como):** Buscando na tabela de check-ins a existência de um registro ativo para a mesma pessoa antes do `save`.
  - **How Much (Quanto custa):** Baixo esforço de desenvolvimento e processamento.
- **Critérios de Aceitação:**
  1. Tentar criar check-in para pessoa com check-in ativo deve retornar erro de validação.
  2. O erro deve conter a mensagem exata: "Esta pessoa já possui um check-in ativo."

### Melhoria 2: Baixa automática do Check-in após Check-out

- **User Story:** Como administrador, eu quero que ao registrar a saída (check-out) de um paciente, o seu check-in seja marcado como inativo automaticamente, para agilizar o fluxo de trabalho e evitar ocupação fantasma.
- **5W2H:**
  - **Who (Quem):** Sistema.
  - **What (O Que):** Mudar o status `active` do Check-in associado para `False`.
  - **When (Quando):** Assim que um novo `Checkout` for salvo com sucesso no banco de dados.
  - **Where (Onde):** No Model de `Checkout` (sobrescrevendo o método `save`).
  - **Why (Por Que):** Manter o banco de dados coerente de forma autônoma.
  - **How (Como):** Acessando a propriedade `self.checkin.active = False` e persistindo a alteração no momento de salvar a saída.
  - **How Much (Quanto custa):** Baixo esforço.
- **Critérios de Aceitação:**
  1. Ao registrar um `Checkout`, o registro de `Checkin` ligado a ele deve ter o campo `active` alterado de `True` para `False` instantaneamente.

### Melhoria 3: Bloqueio de Check-in para Pessoas em Óbito

- **User Story:** Como recepcionista, quero que o sistema me impeça de fazer um check-in para uma pessoa que já possui uma data de óbito registrada, evitando fraudes e inconsistências graves no acolhimento.
- **5W2H:**
  - **Who (Quem):** Sistema / Recepcionista.
  - **What (O Que):** Retornar erro de validação ao tentar hospedar uma `Person` com `death_date` preenchida.
  - **When (Quando):** Na validação de dados pré-cadastro.
  - **Where (Onde):** No Model `Checkin`, método `clean()`.
  - **Why (Por Que):** Evitar erros humanos severos e manter a integridade dos dados históricos.
  - **How (Como):** Validando a propriedade `self.person.death_date`. Se for diferente de nulo, levanta `ValidationError`.
  - **How Much (Quanto custa):** Baixo esforço.
- **Critérios de Aceitação:**
  1. Cadastrar Check-in para pessoa com `death_date` deve ser bloqueado com a mensagem "Não é possível realizar check-in para um paciente em óbito."

### Melhoria 4: Trava de "Serviços da Casa" para pessoas sem Check-in Ativo

- **User Story:** Como administrador, quero que os serviços da casa (refeições/banho) só possam ser lançados para pessoas ativamente na casa, para garantir o controle fidedigno de estoque.
- **5W2H:**
  - **Who (Quem):** Sistema / Atendente.
  - **What (O Que):** Bloquear a criação de `HomeServices` se o indivíduo não estiver hospedado.
  - **When (Quando):** No momento de lançar um novo consumo de serviço.
  - **Where (Onde):** No Model `HomeServices`, método `clean()`.
  - **Why (Por Que):** Assegurar que os custos da casa batam com as pessoas fisicamente presentes.
  - **How (Como):** Fazendo uma query na tabela `Checkin` exigindo `active=True`. Se falso, barra a operação.
  - **How Much (Quanto custa):** Baixo esforço.
- **Critérios de Aceitação:**
  1. Tentar criar serviço de casa para pessoa sem check-in ativo retorna HTTP 400 com a mensagem "A pessoa deve ter um check-in ativo para receber serviços."

---

## Como instalar e rodar o projeto localmente

Siga o passo a passo abaixo para rodar a aplicação na sua máquina (Requisito: Python 3.12+):

### 1. Criar e ativar o ambiente virtual (venv)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / MacOS
source venv/bin/activate
```

### 2. Instalar as dependências atualizadas

```bash
pip install -r requirements.txt
```

### 3. Configurar o banco de dados

```bash
cd danielle
python manage.py makemigrations
python manage.py migrate
```

### 4. Criar administrador e Alimentar com Dados de Teste (Seeds)

```bash
python manage.py createsuperuser
python manage.py loaddata people/seed/people.json
python manage.py loaddata people/seed/checkins.json
python manage.py loaddata people/seed/home-services.json
```

_Nota: Os seeds preenchem dados antigos. Para testar as novas regras de bloqueios ativas, faça inserções pelo Painel Admin._

### 5. Iniciar a aplicação

```bash
python manage.py runserver
```

## Acessando o Sistema

- **Dashboard Público:** http://127.0.0.1:8000/dashboard/
- **Swagger (Documentação da API):** http://127.0.0.1:8000/api/docs/
- **Painel Administrativo:** http://127.0.0.1:8000/admin/
