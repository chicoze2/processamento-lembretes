### Puxar relatorio_mk vendas ontem (definir escopo das empresas)
### tratar as infos
### Fazer os envios api_zap
import json
from mk_api import *
from zap_api import *

payloadMk = {
    "idrelatorioconfiguracao": 248,
    "idrelatorioconsulta": 50,
    "idrelatorioconfiguracaoleiaute": 248,
    "idrelatoriousuarioleiaute": 2010,
    "ididioma": 1,
    "listaempresas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 18, 19, 16, 17],
    "filtros": (
        "EquipeCRM=null;"
        "DesconsiderarEstornadoDevolvido=False;"
        "Cor=null;"
        "SemAutorizacaoExpedicao=True;"
        "ComAutorizacaoExpedicao=True;"
        "Tipodevenda=null;"
        "Periododamovimentacaofinal=2024-11-19 00:00;"
        "ComExpedicao=True;"
        "SemExpedicao=True;"
        "Modelodoveiculo=6207,5922,5921,5920,5919,5918,5917,5916,5915,5914,5913,5912,5911,5910,5909,5908,5907,5906,5905,6400,6401,6402,6403,6404,6405,6406,6407,6408,6409,6410,6411,6412,6413,6414,6415,6416,6417,6418,5444,5445,5446,5447,5448,5449,5436,6004,5437,5438,5439,5450,5451,5452,5566,5440,5441,5442,5443,2019,2104,2313,2522,2731,2940,3149,3358,3567,3776,3985,4194,4403,5039,5264,5578,2018,2017,6016,4878,2023,2024,2025,2137,2346,2555,2764,2973,3182,3391,3600,3809,4018,4227,6017,5579,5103,4436,2262,2680,2889,3098,3307,3516,3725,3934,4143,4352,4561,5055,5742,6180,4830,2053,2054,2055,2471;"
        "Tipodemovimento=2,25,26,22,11,9,17,10,21,32;"
        "Municipio=null;"
        "Consorcio=null;"
        "TipoVeiculo=null;"
        "Pessoa=null;"
        "Estadodoveiculo=null;"
        "Periododamovimentacaoinicial=2024-11-18 00:00;"
        "TipoPessoa=null;"
        "Pontodevendadovendedor=null;"
        "FinanceiraLeasing=null;"
        "FinanceiraCalculo=null;"
        "Origemdavenda=null;"
        "Vendedor=null;"
        "MovimentosCancelados=False"
    )
}

response = make_request(payloadMk)

print(response)

try:
    for lead in response:
        try:
            if isinstance(lead['telefonecelular'], str):
                nome = lead['pessoa']
                modelo = lead['modelo']
                vendedor = lead['vendedor'].split(" ")[0].capitalize()
                celular = lead['telefonecelular'].replace("(", "").replace(")", "").replace(" ", "").replace("-", "")

                mensagem = f"""Olá, *{nome}!* Tudo bem? 😁 Sou Simone Alves, Especialista em Seguros da Universo Honda.
Parabéns pela conquista da sua *{modelo}* 🏍 com o(a) nosso(a) consultor(a) *{vendedor}*!

Que tal fazer uma cotação de seguro para proteção de sua mais nova conquista😃
Basta preencher o formulário com os dados do principal condutor, e logo te retorno com valores sem compromisso. 😉


https://forms.gle/sZqvKJDmxdg8wXjZ8

Quando terminar, é só enviar um "OK" aqui que prosseguimos. :) 
""" 

                payloadChat = {
                                "queueId": 14,
                                "apiKey": "297777cef57647888a9c5f26b4ecc751",
                                "number": "55" + celular,
                                "markerId": 11    
                }
                chat = open_chat(payload=payloadChat)
                print(chat)
                chatId = chat['chatId']

                payloadMsg = {
                "queueId": 14,
                "apiKey": "297777cef57647888a9c5f26b4ecc751",
                "chatId": chatId,
                "text": mensagem }

                msg = send_message(payloadMsg)
                print(msg)

        except Exception as e:
            print(f"(process_seguro) Ocorreu um erro ao iterar um lead. {e}")   

except Exception as e:
    print(f"Ocorreu um erro no loop principal {e}")