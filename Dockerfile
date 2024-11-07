FROM rasa/rasa:latest-full

# Define o diretório de trabalho
WORKDIR /app

# Copia o conteúdo do projeto para o diretório de trabalho no container
COPY . /app

# Instala as dependências do requirements.txt, incluindo o modelo SpaCy
RUN pip install -r requirements.txt

# Treina o modelo do Rasa
RUN rasa train

# Executa o servidor do Rasa com a API habilitada e CORS
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
