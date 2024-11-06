import pandas as pd
import json

def obter_valor_revisao_mock(modelo):
    # Carregar dados do arquivo JSON
    with open('api/src/revisoes.json', 'r') as file:
        valores_revisao = json.load(file)
    
    valor_revisao = valores_revisao[modelo]['primeira_revisao']
    
    return float(valor_revisao.replace(',', '.'))

df = pd.read_excel('output/pendentes_consolidados.xlsx')

# Lista para armazenar mensagens
mensagens = []

# Iterar sobre cada registro
for index, row in df.iterrows():
    modelo = row['modelo'] 
    nome_raw = row['pessoa'] 
    nome = nome_raw.split()[0].title()
    telefone = row['telefonecelularformatado'].replace('-', '').replace(' ', '').replace('(', '').replace(')', '')

    # try:
    #     valor_revisao = obter_valor_revisao_mock(modelo)
    # except:
    #     valor_revisao=1999.99
        
    mensagem = f"""Olá {nome}, parabéns pela aquisição da sua *Honda {modelo}!*

Você sabia que a 1ª revisão da sua motocicleta é essencial para manter a garantia de até três anos?

Ela deve ser realizada em até 6 meses ou 1.000 km rodados.

Gostaria de agendar agora a sua revisão? 

É rápido e fácil!"""


    mensagens.append({'telefone': telefone, 'mensagem': mensagem})


## salvar resultado como CSV
df_mensagens = pd.DataFrame(mensagens)
df_mensagens.to_csv('output/mensagens.csv', index=False)
 