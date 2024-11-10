# Chatbot sobre TEA

----------------------------------------------------------------------------------------------------------------------------

### Um chatbot desenvolvido com `Rasa` para responder perguntas sobre o autismo, promovendo informações confiáveis e conscientização.

#### Dependências:

1. Python 3.10
2. Rasa 3.6.2
3. Outras dependências listadas em `requirements.txt` e `actions/requirements.txt`

#### Execute na sua máquina local:

* `git clone https://github.com/whalisson/Projeto-Chatbot.git`
* `cd Projeto-Chatbot`
* `python3.10 -m venv venv`
* `source venv/bin/activate` *(No Windows use: `venv\\Scripts\\activate`)*
* `pip install -r requirements.txt`
* `pip install -r actions/requirements.txt`
* `rasa train` *(Se quiser retreinar o modelo, caso contrário ignore)
* `rasa run actions`
* `rasa shell`

### Explicações dos Passos:

1. **Clone o repositório**: Baixa o código do projeto do GitHub.
2. **Entre no diretório do projeto**: Navega para a pasta do projeto clonado.
3. **Crie um ambiente virtual**: Configura um ambiente virtual isolado para gerenciar as dependências.
4. **Ative o ambiente virtual**: Inicia o ambiente virtual para que as instalações sejam locais a ele.
5. **Instale as dependências**: Adiciona os pacotes necessários ao ambiente virtual.
6. **Treine o modelo Rasa**: Cria o modelo de entendimento baseado nos dados do projeto.
7. **Inicie o servidor de ações**: Executa o servidor para funcionalidades personalizadas.
8. **Execute o chatbot**: Interaja com o chatbot no terminal.