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
    "listaempresas": [3, 4, 5, 6, 7, 9, 11, 13, 18, 16, 17],
    "filtros": "EquipeCRM=null;DesconsiderarEstornadoDevolvido=False;Cor=null;SemAutorizacaoExpedicao=True;ComAutorizacaoExpedicao=True;Tipodevenda=null;Periododamovimentacaofinal=2024-11-22 00:00;ComExpedicao=True;SemExpedicao=True;Modelodoveiculo=null;Tipodemovimento=2,25,26,22,11,9,17,10,21,32;Municipio=null;Consorcio=null;TipoVeiculo=null;Pessoa=null;Estadodoveiculo=null;Periododamovimentacaoinicial=2024-11-21 00:00;TipoPessoa=null;Pontodevendadovendedor=null;FinanceiraLeasing=null;FinanceiraCalculo=null;Origemdavenda=null;Vendedor=null;MovimentosCancelados=False"
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