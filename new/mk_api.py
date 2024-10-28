import requests
import os
from dotenv import load_dotenv



def make_request(body):

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    base_url = os.getenv('API_URL')
    headers = {
        'Content-Type': 'application/json',
        'Host': 'microworkcloud.com.br',
        'Authorization': f'Bearer {os.getenv("API_KEY")}'
    }

    try:
        response = requests.post(base_url, headers=headers, json=body)
        return response.json()
    except Exception as e: 
        print(f"(mk_api) - Ocorreu um erro ao disparar o request. {e}")

