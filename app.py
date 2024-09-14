from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# URL do servidor Rasa
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    # Obtém a mensagem do usuário do corpo da solicitação JSON
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"response": "Mensagem do usuário não fornecida."})
    
    try:
        # Enviar mensagem do usuário para o Rasa
        rasa_response = requests.post(RASA_SERVER_URL, json={"sender": "user", "message": user_message})
        
        # Verifica se a resposta do Rasa é bem-sucedida
        if rasa_response.status_code == 200:
            rasa_messages = rasa_response.json()
            if rasa_messages:
                # Coleta todas as mensagens retornadas do Rasa
                responses = []
                for message in rasa_messages:
                    # Adiciona cada mensagem à lista de respostas
                    response_text = message.get("text", "Desculpe, não consegui entender.")
                    responses.append(response_text)
                # Junta todas as mensagens em uma única resposta
                return jsonify({"response": " ".join(responses)})
        return jsonify({"response": "Ocorreu um erro ao se comunicar com o servidor Rasa."})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"response": f"Erro de requisição: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
