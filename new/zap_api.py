import requests

def open_chat(payload, headers=None):
    try:
        print("Enviando lead para fila do chat")
        response = requests.post("https://universohonda.atenderbem.com/int" + '/openChat', json=payload, headers=headers)
        return response.json() # Return the response in JSON format (if applicable)

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            ## fazer request para descobrir ID do chat existente
            print(response.json())
            print("Já existe atendimento com esse num.")
            return None
        elif response.status_code == 404:
            print("Numero informado não possui whatsapp")
            return None
        else:
            print(f"HTTP error occurred: (chat){http_err}")
            return None
    except Exception as err:
        print(f"An error occurred: {err}")

def send_message(payload, headers=None):
    try:
        print("Enviando mensagem no chat")
        response = requests.post("https://universohonda.atenderbem.com/int" + '/sendMessageToChat', json=payload, headers=headers)
        return response.json() # Return the response in JSON format (if applicable)

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print("Chat nao encontrado na fila.")
            return
        else:
            print(f"HTTP error occurred: (mensagem){http_err}")
            return
    except Exception as err:
        print(f"An error occurred: {err}")

def send_opportunity(payload, headers=None):
    try:

        print("Enviando lead para CRM ")
        response = requests.post("https://universohonda.atenderbem.com/int" + '/createOpportunity', json=payload, headers=headers)
        
        response.raise_for_status()  # Check if the request was successful        
        return response.json() # Return the response in JSON format (if applicable)
    
    except requests.exceptions.HTTPError as http_err:
        print('error handler - API send_opportunity')
        print(f"HTTP error occurred: (opportunity){http_err}")
        print(payload)
        print('===========================================')
    except Exception as err:
        print(f"An error occurred: {err}")

