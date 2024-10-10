import requests
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

def make_request(body):

    base_url = os.getenv('API_URL')
    headers = {
        'Content-Type': 'application/json',
        'Host': 'microworkcloud.com.br',
        'Authorization': f'Bearer {os.getenv("API_KEY")}'
    }


    response = requests.post(base_url, headers=headers, json=body)
    return response.json()

body = {
    "idrelatorioconfiguracao": 248,
    "idrelatorioconsulta": 50,
    "idrelatorioconfiguracaoleiaute": 248,
    "idrelatoriousuarioleiaute": 1968,
    "ididioma": 1,
    "listaempresas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 18, 19, 16, 17],
    "filtros": (
        "EquipeCRM=null;"
        "DesconsiderarEstornadoDevolvido=False;"
        "Cor=null;"
        "SemAutorizacaoExpedicao=True;"
        "ComAutorizacaoExpedicao=True;"
        "Tipodevenda=null;"
        "Periododamovimentacaofinal=2024-10-09 00:00;"
        "ComExpedicao=True;"
        "SemExpedicao=True;"
        "Modelodoveiculo=null;"
        "Tipodemovimento=2,25,26,22,11,9,17,10,21,32;"
        "Municipio=null;"
        "Consorcio=null;"
        "TipoVeiculo=null;"
        "Pessoa=null;"
        "Estadodoveiculo=null;"
        "Periododamovimentacaoinicial=2024-10-09 00:00;"
        "TipoPessoa=null;"
        "Pontodevendadovendedor=null;"
        "FinanceiraLeasing=null;"
        "FinanceiraCalculo=null;"
        "Origemdavenda=null;"
        "Vendedor=null;"
        "MovimentosCancelados=False"
    )
}

