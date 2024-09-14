import google.generativeai as genai
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from dotenv import load_dotenv
import os

# Carrega o conteúdo do arquivo .env
load_dotenv()

# Configurar a API do Gemini
genai.configure(api_key=os.getenv("API_KEY"))

class ActionAskGemini(Action):
    def name(self) -> str:
        return "action_ask_gemini"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Captura a última mensagem do usuário
        user_message = tracker.latest_message.get('text')

        try:
            # Inicializa o modelo Gemini
            model = genai.GenerativeModel('gemini-pro')

            # Gera a resposta para a pergunta do usuário
            response = model.generate_content(user_message)

            # Envia a resposta gerada pelo Gemini ao usuário
            dispatcher.utter_message(text=response.text)

        except Exception as e:
            # Se algo der errado, envia uma mensagem de erro
            dispatcher.utter_message(text="Desculpe, não consegui obter uma resposta no momento.")
            print(f"Erro ao usar Google Gemini: {e}")

        return []