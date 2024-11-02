import google.generativeai as genai
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from dotenv import load_dotenv
import os
from typing import Any, Text, Dict, List

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
    
class ActionAskFamilyMember(Action):
    def name(self) -> Text:
        return "action_ask_family_member"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Verifica se o slot family_member está vazio
        if not tracker.get_slot('family_member'):
            dispatcher.utter_message(text="Quem está passando pela crise, seu filho ou filha?")
        
        return []

import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionProvideScientificInfo(Action):

    def name(self) -> Text:
        return "action_provide_scientific_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Obtenha a última mensagem do usuário (a pergunta)
        user_message = tracker.latest_message.get('text')

        # Chame a API do PubMed para buscar artigos científicos
        articles = self.get_pubmed_articles(user_message)

        # Verifique se encontramos algum artigo
        if articles:
            response = f"Encontrei alguns artigos científicos relevantes sobre autismo:\n\n"
            for article in articles[:3]:  # Mostra até 3 artigos
                response += f"Título: {article['title']}\nLink: {article['link']}\n\n"
        else:
            response = "Desculpe, não encontrei artigos científicos relevantes para sua pergunta."

        dispatcher.utter_message(text=response)
        return []

    def get_pubmed_articles(self, query: Text) -> List[Dict[Text, Any]]:
        """
        Faz uma chamada à API do PubMed para buscar artigos sobre autismo
        relacionados à consulta do usuário.
        """
        # URL base da API E-utilities do PubMed
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        
        # Parâmetros da consulta
        params = {
            "db": "pubmed",            # Banco de dados
            "term": "autism",             # Termo de busca (a pergunta do usuário)
            "retmode": "json",         # Retornar em formato JSON
            "retmax": 5,               # Número máximo de artigos a retornar
        }

        response = requests.get(base_url, params=params)

        # Adicione um print para depurar o resultado da resposta da API
        print(f"Resposta da API PubMed (esearch): {response.text}")

        if response.status_code == 200:
            data = response.json()

            if "esearchresult" in data and "idlist" in data["esearchresult"]:
                # Se IDs de artigos forem encontrados, faça uma segunda chamada para obter detalhes
                article_ids = data["esearchresult"]["idlist"]
                return self.get_article_details(article_ids)
        return []

    def get_article_details(self, article_ids: List[Text]) -> List[Dict[Text, Any]]:
        """
        Busca detalhes dos artigos com base nos IDs fornecidos pela primeira chamada.
        """
        if not article_ids:
            return []

        # URL base para buscar os detalhes dos artigos
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        
        # Parâmetros para buscar os detalhes dos artigos
        params = {
            "db": "pubmed",
            "id": ",".join(article_ids),  # IDs dos artigos
            "retmode": "json",
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()

            articles = []
            if "result" in data:
                for article_id in article_ids:
                    if article_id in data["result"]:
                        article_data = data["result"][article_id]
                        articles.append({
                            "title": article_data.get("title", "Sem título"),
                            "link": f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/"
                        })
            return articles
        return []
