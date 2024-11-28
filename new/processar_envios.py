import requests
import pandas as pd

from zap_api import *
# Carregar CSV
df = pd.read_csv("out/mensagens.csv")
for index, row in df.iterrows():
    
    try:
        nome = row['nome']
        numero = int(row['telefone'])
        mensagem = row['mensagem']
        etiqueta = row['etiqueta']
        chassi = row['chassi']
        disparo = row['disparo']
        cidade = row['cidade']

        ### envio oportunidade
        try:
            leadOpportunity = {
                "queueId": 57,
                "apiKey": "f59f332a2c5827556c9782e1c3b3c0a6",
                "responsableid": 540,
                "title": nome + "" +  chassi,
                "fkPipeline": 6,
                "fkStage": disparo,
                "mainphone": "55" + str(numero),
                "description": cidade,
            }

            send_opportunity(leadOpportunity)

        except Exception as e:
            print(f"Ocorreu um erro na requisição criar oportunidade")
            print(e)
            print(leadOpportunity)

        ## ENVIO CHAT
        try:
            print(f"Enviando mensagem para o número: {numero}")

            payload_chat = {
            "queueId": 57,
            "apiKey": "bf99d8f0ffa04849920e9375797741fe",
            "number": f"{numero}",
            "markerId": etiqueta
        }
            response = requests.post("https://universohonda.atenderbem.com/int/openChat", 
                                     json=payload_chat, timeout=10, headers=None)  # 10 segundos de timeout

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                response_data = response.json()  # Converte a resposta para JSON
                chatId = response_data.get("chatId")

                if chatId:
                    payload_mensagem = {
                        "queueId": 57,
                        "apiKey": "f59f332a2c5827556c9782e1c3b3c0a6",
                        "chatId": chatId,
                        "text": mensagem
                    }

                    # Enviar a mensagem
                    resposta_envio = send_message(payload_mensagem)
                    print(f"Mensagem enviada: {resposta_envio}")

                else:
                    print(f"Erro: chatId não encontrado para o número {numero}")
            else:
                print(f"Erro na requisição ao abrir o chat: {response.status_code} - {response.text}")

            

        except requests.exceptions.Timeout:
            print(f"chat - Timeout ao tentar abrir o chat para o número: {numero}")
        except requests.exceptions.RequestException as e:
            print(f"chat - Erro ao fazer a requisição: {e}")

    except Exception as e:
        print(f"Ocorreu um erro dentro do loop principal {e}")