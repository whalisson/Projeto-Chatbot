FROM rasa/rasa:latest-full

# Define o diretório de trabalho
WORKDIR /app

# Copia o conteúdo do projeto para o container
COPY . /app

# Instala o modelo SpaCy necessário
RUN python -m spacy download pt_core_news_md

# Treina o modelo do Rasa
RUN rasa train

# Executa o servidor do Rasa com a API habilitada e CORS
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
