FROM rasa/rasa:latest-full
WORKDIR /app
COPY . /app


RUN mkdir -p /app/.rasa && chmod -R 777 /app/.rasa

RUN pip install -r requirements.txt

CMD ["bash", "-c", "rasa train && rasa run --enable-api --cors '*' --port 5005"]
