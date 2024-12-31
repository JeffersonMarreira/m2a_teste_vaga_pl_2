<h1 align="center">Teste de Programação - Nível Pleno</h1>
<p align="center"><i>Aplicação: Controle de Ponto Eletrônico</i></p>

![Static Badge](https://img.shields.io/badge/python-blue)
![Static Badge](https://img.shields.io/badge/orm-django-3fb950)

## Objetivo

Desenvolver um sistema simples de ponto eletrônico que permita registrar e consultar batidas de entrada, saída e intervalo de funcionários de diferentes empresas. O sistema deve ser construído usando Django e deve incluir funcionalidades básicas, com foco em qualidade de código, boas práticas e experiência do usuário.

## Pré-requisitos

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configuração do Ambiente

1. Clone o repositório para a sua máquina local:

    ```sh
    git clone https://github.com/daniel-root/m2a_teste_vaga_pl_2/tree/feature/eletronic_time_clock
    cd m2a_teste_vaga_pl_2
    ```

2. Crie um ambiente virtual:

    ```sh
    python -m venv .venv
    source .venv/bin/activate  # Linux e macOS
    .venv\Scripts\activate     # Windows
    ```

3. Instale as dependências do projeto:

    ```sh
    pip install -r requirements.txt
    ```

4. Renomeei o arquivo `.env.example` para `.env` e configure as variáveis de ambiente contidas no arquivo:

    ```plaintext
    DEBUG=on
    SECRET_KEY=your-secret-key-here
    ENGINE=postgresql
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    PGADMIN_EMAIL=your_pgadmin_email@example.com
    PGADMIN_PASSWORD=your_pgadmin_password
    ```

## Migrações e Coleta de Arquivos Estáticos

1. Faça as migrações do banco de dados:

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

2. Colete os arquivos estáticos:

    ```sh
    python manage.py collectstatic
    ```

3. Crie um superusuário para acessar o painel de administração do Django:

    ```sh
    python manage.py createsuperuser
    ```

## Executando o Projeto com Docker

1. Construa e inicie os containers Docker:

    ```sh
    docker compose up --build -d
    ```

2. Acesse o projeto no navegador através do endereço: `http://localhost:8080`

## Acessando o PgAdmin

1. Acesse o PgAdmin no navegador através do endereço: `http://localhost:5050`

2. Use as credenciais do arquivo `.env` para fazer login.

## Rodando os Testes

Para rodar os testes e verificar se tudo está funcionando corretamente, execute o seguinte comando:

  ```sh
  python manage.py test
  ```