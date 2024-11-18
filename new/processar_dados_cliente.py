import pandas as pd
from mk_api import make_request

## receber periodo
## receber relatorio IHS
## fazer requests na api microwork dentro do periodo

def process_relatorios(periodo_inicial, periodo_final, relatorio_ihs_path):
    relatorio_ihs_pendentes = pd.read_csv(relatorio_ihs_path, sep='|')
    
    body = {
        "idrelatorioconfiguracao": 248,
        "idrelatorioconsulta": 50,
        "idrelatorioconfiguracaoleiaute": 248,
        "idrelatoriousuarioleiaute": 1968,
        "ididioma": 1,
        "listaempresas": [1,2,3,4,5,6,7,8,9,10,11,13,14,18,19,16,17],
        "filtros": (
            "EquipeCRM=null;"
            "DesconsiderarEstornadoDevolvido=False;"
            "Cor=null;"
            "SemAutorizacaoExpedicao=True;"
            "ComAutorizacaoExpedicao=True;"
            "Tipodevenda=null;"
            f"Periododamovimentacaofinal={periodo_final} 00:00;"
            "ComExpedicao=True;"
            "SemExpedicao=True;"
            "Modelodoveiculo=null;"
            "Tipodemovimento=2,9,11,17,21,25,26,32,10,22;"
            "Municipio=null;"
            "Consorcio=null;"
            "TipoVeiculo=null;"
            "Pessoa=null;"
            "Estadodoveiculo=null;"
            f"Periododamovimentacaoinicial={periodo_inicial} 00:00;"
            "TipoPessoa=null;"
            "Pontodevendadovendedor=null;"
            "FinanceiraLeasing=null;"
            "FinanceiraCalculo=null;"
            "Origemdavenda=null;"
            "Vendedor=null;"
            "MovimentosCancelados=False"
        )
    }
    realatorio_vendas = make_request(body)

    df_vendas = pd.DataFrame(realatorio_vendas)

    # Filtrar os chassis do relatório pendente usando a coluna correta
    chassis_pendentes = relatorio_ihs_pendentes['CHASSI_VENDIDO'].tolist()

    # Verificar quais chassis do relatorio pendente não estão presentes nas vendas
    chassis_faltantes = [chassi for chassi in chassis_pendentes if chassi not in df_vendas['chassi'].tolist()]
    
    # Salvar os chassis faltantes em um arquivo de texto
    with open('out/chassis_faltando_info_cliente.txt', 'w') as f:
        for chassi in chassis_faltantes:
            f.write(f"{chassi}\n")
    
    # Remover os chassis faltantes do DataFrame de pendentes de revisao
    pendentes_consolidados = relatorio_ihs_pendentes[~relatorio_ihs_pendentes['CHASSI_VENDIDO'].isin(chassis_faltantes)]

    #juntar as informacoes (chass com nome etc...)
    info_consolidado = pd.merge(pendentes_consolidados, pd.DataFrame(realatorio_vendas), left_on='CHASSI_VENDIDO', right_on='chassi', how='left')
    info_consolidado = info_consolidado.drop(columns=['NOME_CLIENTE', 'TELEFONE_RESIDENCIAL', 'TELEFONE_COMERCIAL', 'RAMAL', 'E_MAIL'])

    info_consolidado.to_excel('out/consolidados.xlsx')

# process_relatorios("2024-05-01", "2024-10-23", "./taubate_out.txt")

def make_message(modelo, nome, delta_D: str):
    mensagem = ""
    delta_DInt = int(delta_D)

    if 23 <= delta_DInt <= 29: ## Primeiro
        disparo = 39
        etiqueta = 35
        mensagem = f"""Olá {nome}, parabéns pela aquisição da sua *Honda {modelo}!*

Você sabia que a 1ª revisão da sua motocicleta é essencial para manter a garantia de até três anos?

Ela deve ser realizada em até 6 meses ou 1.000 km rodados.

Gostaria de agendar agora a sua revisão? 

É rápido e fácil!"""
    elif 83 <= delta_DInt <= 89: ## Segundo
        disparo = 41
        etiqueta = 36
        mensagem = f"""Olá {nome}! 

Lembramos que a primeira revisão da sua *Honda {modelo}* está chegando. 

Ela vence em 6 meses ou 1000 km rodados, o que ocorrer primeiro. Não se esqueça de realizar a revisão para garantir a manutenção da garantia da sua moto. 

Deseja agendar agora?"""
    elif 153 <= delta_DInt <= 159: ## Terceiro
        disparo = 42
        etiqueta = 37
        mensagem = f"""Olá {nome}! 

Faltam 30 dias para o vencimento da primeira revisão da sua *Honda {modelo}!**

Lembre-se, é essencial realizá-la em até 6 meses ou 1000 km rodados, para manter a garantia da sua moto. 

Deseja agendar agora?

"""
    elif 173 <= delta_DInt <= 179: ## Quarto
        disparo = 43
        etiqueta = 38
        mensagem = f"""Olá {nome}! 

Última chance para realizar a primeira revisão da sua *Honda {modelo}.*

O prazo de 6 meses está quase acabando. 

Garanta a manutenção da sua garantia agendando agora mesmo por aqui!
"""

    else:
        return None, None, None
        print(f"Ignorado {nome} - {delta_D} dias" )

    return mensagem, etiqueta, disparo


def process_messages(relatorio_consolidado_path):
    relatorio_consolidado = pd.read_excel(relatorio_consolidado_path)

    mensagens_processadas = []

    for index, row in relatorio_consolidado.iterrows():
        try:
            modelo = row['modelo'] 
            delta_D = row['DIAS_APOS_A_VENDA'] 
            chassi = row['chassi']
            cidade = row['municipiouf']
            nome_raw = row['pessoa'] 
            nome = nome_raw.split()[0].title()
            telefone = str(row['telefonecelularformatado']).replace('-', '').replace(' ', '').replace('(', '').replace(')', '')

            print(f"{telefone} + {nome}")
            mensagem, etiqueta, disparo = make_message(modelo, nome, delta_D)

            if etiqueta != None:
                if telefone != "":
                    mensagens_processadas.append({'telefone': telefone, 'mensagem': mensagem, 'etiqueta': etiqueta, 'chassi': chassi, 'nome' : nome, 'disparo' : disparo, 'cidade': cidade})
    

        except Exception as e:
            print(f"Ocorreu um erro dentro do loop process messages {e}")

    df_mensagens = pd.DataFrame(mensagens_processadas)
    df_mensagens.to_csv('out/mensagens.csv', index=False)

process_relatorios('2024-06-06', '2024-11-18', 'taubate_nov3.txt')
process_messages('out/consolidados.xlsx')



