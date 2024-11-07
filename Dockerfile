FROM rasa/rasa:latest-full

# Define o diretório de trabalho
WORKDIR /app

# Copia o conteúdo do projeto para o diretório de trabalho no container
COPY . /app

# Copia o modelo SpaCy local para o ambiente do Docker
COPY spacy_models/pt_core_news_md /usr/local/lib/python3.10/site-packages/spacy/data/pt_core_news_md

# Configura a variável de ambiente para o SpaCy localizar o modelo
ENV SPACY_DATA_PATH=/usr/local/lib/python3.10/site-packages/spacy/data

# Treina o modelo do Rasa
RUN rasa train

# Executa o servidor do Rasa com a API habilitada e CORS
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
