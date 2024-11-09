# Usar a imagem oficial do Python 3.10
FROM python:3.10-slim

# Definir o diretório de trabalho
WORKDIR /app

# Atualizar o pip para a versão mais recente
RUN pip install --no-cache-dir --upgrade pip

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Rasa
RUN pip install --no-cache-dir rasa==3.6.20

# Copiar arquivos do projeto para o container
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta padrão do Rasa
EXPOSE 5005

# Definir o comando para iniciar o servidor Rasa
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
