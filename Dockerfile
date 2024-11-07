FROM rasa/rasa:latest-full
WORKDIR /app
COPY . /app
RUN rasa train
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
