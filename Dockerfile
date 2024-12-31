# baixar imagem base oficial
FROM python:3.11-slim-buster

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev 
RUN cd /usr/local/bin 
RUN ln -s /usr/bin/python3 python 
RUN pip3 install --upgrade pip 
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# instalar dependências
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copiar projeto
COPY . .
