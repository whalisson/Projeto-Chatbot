# Usa uma imagem base com Python 3.10
FROM python:3.10-slim

# Configura o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . /app

# Atualiza o pip e instala as dependências necessárias para o Rasa
RUN pip install --upgrade pip

# Instala pacotes de compilação e outras dependências de sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala o Rasa e outras dependências específicas
RUN pip install rasa==3.6.20 spacy==3.7.6

# Instala as dependências do projeto do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Treina o modelo Rasa (opcional)
RUN rasa train

# Executa o servidor do Rasa
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
