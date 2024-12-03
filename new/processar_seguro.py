### Puxar relatorio_mk vendas ontem (definir escopo das empresas)
### tratar as infos
### Fazer os envios api_zap
import json
from mk_api import *
from zap_api import *

data_inicio = "2024-11-30"
data_final =  "2024-12-03"

payloadMk = {
    "idrelatorioconfiguracao": 248,
    "idrelatorioconsulta": 50,
    "idrelatorioconfiguracaoleiaute": 248,
    "idrelatoriousuarioleiaute": 2016,
    "ididioma": 1,
    "listaempresas": [3, 4, 5, 6, 7, 9, 11, 13, 18, 16, 17],
    "filtros": f"EquipeCRM=null;DesconsiderarEstornadoDevolvido=False;Cor=null;SemAutorizacaoExpedicao=True;ComAutorizacaoExpedicao=True;Tipodevenda=null;Periododamovimentacaofinal={data_final} 00:00;ComExpedicao=True;SemExpedicao=True;Modelodoveiculo=5751,5420,6198,5435,5419,5421,5422,5423,5424,5425,5426,5427,5428,5429,5430,5431,5432,5433,5434,2335,5240,5715,10,11,12,2126,2544,2753,2962,3171,3380,3589,3798,4007,4216,4425,5015,6152,6161,5249,14,5024,5724,13,15,2123,2332,2541,2750,2959,3168,3377,3586,3795,4004,4213,4422,5919,5906,5905,5922,5921,5920,5918,5917,5916,5915,5914,6207,5913,5912,5911,5910,5909,5908,5907,6409,6411,6412,6413,6414,6415,6416,6417,6418,6400,6401,6402,6403,6404,6405,6406,6407,6408,6410,2385,3221,3012,3430,3639,2803,3848,4057,4266,2594,2176,159,4475,6150,5013,158,157,5713,5238,5251,4339,5726,6163,4130,5026,4548,1406,1407,1408,2249,2458,2667,2876,3085,3294,3503,3712,3921,3013,2804,2595,2386,2177,147,146,145,5011,5729,5236,6166,4476,4267,4058,3849,3640,3431,3222,152,4473,6151,5014,5239,5714,4264,4055,3846,3637,3428,3219,3010,2801,2592,2383,2174,153,151,6184,1416,1417,1418,2248,2457,2666,2875,3084,3293,3502,3711,3920,4129,4338,4547,5029,5254,5746,2246,2664,1401,3082,5058,3291,2873,4833,4545,4336,4127,3918,5739,6177,1402,3709,3500,2455,1403,5416,6188,5750,5404,5405,5406,5407,5408,5409,5410,5411,5412,5413,5414,5415,5402,5403,5417,5418,2346,4878,6017,2137,5579,2025,4436,4227,2024,2023,4018,3809,3600,3391,3182,2764,2973,5103,2555,5055,6180,4830,2053,2054,2055,2262,2471,2680,2889,3098,3307,3516,3725,3934,4143,4352,4561,5742,2031,2139,2348,2557,3393,5092,4229,2766,2975,3184,3602,3811,4020,4438,6006,5568,4867,2029,2030,4581,4582,4583,4584,4585,4578,4586,4576,4587,4579,4588,4589,5257,4577,5736,4590,5032,6173,4580,5973,4350,4141,3932,3723,3514,3305,3096,2887,2678,2469,2260,1984,1983,1982,4832,5057,4559,5535,6209,5848,5847,5846,5845,5844,5843,5842,5841,5840,5839,5838,5837,5836,5835,5850,5834,5833,5849,6345,6361,6360,6359,6358,6357,6356,6355,6354,6353,6352,6351,6350,6349,6348,6347,6346,6344,6343,6375,6376,6368,6367,6362,6363,6364,6369,6377,6378,6370,6371,6379,6380,6372,6373,6374,6365,6366,2094,4862,5752,2512,6189,5087,1391,2721,4393,4184,3975,3766,3557,3348,3139,2930,1392,1393,2303,5831,5816,5832,5815,5819,6201,5818,5817,5820,5821,5822,5823,5824,5825,5826,5827,5828,5829,5830,5813,5797,5798,5799,5800,5801,5802,5803,5804,5805,5806,5807,5808,5809,5810,5811,5812,5814,6200,5786,5787,5788,5784,5783,5782,5790,5781,5791,5780,5792,5793,5794,5795,5796,6199,5779,5789,5785;Tipodemovimento=2,25,26,22,11,9,17,10,21,32;Municipio=null;Consorcio=null;TipoVeiculo=null;Pessoa=null;Estadodoveiculo=null;Periododamovimentacaoinicial={data_inicio} 00:00;TipoPessoa=null;Pontodevendadovendedor=null;FinanceiraLeasing=null;FinanceiraCalculo=null;Origemdavenda=null;Vendedor=null;MovimentosCancelados=False"
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