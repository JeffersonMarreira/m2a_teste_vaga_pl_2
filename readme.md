<h1 align="center">Teste de Programação - Nível Pleno</h1>

<p align="center"><i>Aplicação: Controle de Ponto Eletrônico</i></p>

![Static Badge](https://img.shields.io/badge/python-blue)
![Static Badge](https://img.shields.io/badge/orm-django-3fb950)
![Static Badge](https://img.shields.io/badge/report-PyMuPDF-DAA520)

## Objetivo
Desenvolver um sistema simples de ponto eletrônico que permita registrar e consultar batidas de entrada, saída e intervalo de funcionários de diferentes empresas. O sistema deve ser construído usando Django e deve incluir funcionalidades básicas, com foco em qualidade de código, boas práticas e experiência do usuário.

## Requisitos do Sistema

### 1. Modelagem de Dados
- **Model `Empresa`**:
  - Campos: `nome`, `endereco`, `telefone`
  
- **Model `Funcionario`**:
  - Campos: `nome`, `email`, `empresa` (chave estrangeira para o modelo Empresa)
  
- **Model `Ponto`**:
  - Campos: `funcionario` (chave estrangeira para o modelo Funcionario), `data`, `entrada`, `saida`, `intervalo`
  - Métodos para calcular horas trabalhadas e atrasos/horas extras.

### 2. Funcionalidades
- **Página Inicial**:
  - Permitir que o usuário selecione uma empresa existente ou cadastre uma nova.
  
- **Gerenciamento de Empresas**:
  - Cadastrar e atualizar informações de empresas.
  
- **Gerenciamento de Funcionários**:
  - Cadastrar e atualizar informações de funcionários associados a uma empresa.
  
- **Registro de Batidas**:
  - Página para registrar batidas de ponto (entrada, saída e intervalo) para funcionários.
  
- **Consulta de Batidas**:
  - Página para visualizar as batidas registradas, com a possibilidade de filtrar por data e funcionário.

### 3. Interface de Usuário
- Usar Django Templates para criar as páginas. A aparência deve ser simples, mas funcional, podendo utilizar CSS ou um framework como Bootstrap para melhorar a usabilidade.
- Fornecer feedback ao usuário após ações (como mensagens de sucesso ou erro).

### 4. Relatórios
- Criar uma funcionalidade para gerar relatórios de batidas utilizando PyMuPDF (ou uma biblioteca similar). O relatório deve incluir as batidas de ponto registradas, horas trabalhadas, atrasos e horas extras, formatado de maneira legível.

### 5. Autenticação
- Implementar um sistema básico de autenticação para usuários (funcionários), permitindo registro e login.

### 6. Testes Automatizados
- Implementar testes básicos para o modelo e as views, usando `pytest` ou `unittest`. Os testes devem cobrir:
  - Validação dos dados do modelo.
  - Funcionalidade de registro e consulta de batidas.

### 7. Documentação
- Incluir um `README.md` com instruções sobre como configurar o ambiente, instalar dependências e rodar o projeto.
- Documentar funções e classes usando docstrings.
