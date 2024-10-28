import pandas as pd
from new.mk_api import make_request

relatorio_txt = 'output/taubate_maio.txt'
output_faltantes_txt = 'output/chassis_faltantes.txt'
output_excel_consolidados = 'output/pendentes_consolidados.xlsx'

def processar_ihs(delta_D):
    # Abrir os dados do relatorio de revisoes pendentes no IHS.
    relatorio_pendentes = pd.read_csv(relatorio_txt, sep='|')
    
    # Configurar o corpo da requisição para o relatório de vendas
    body = {
        "idrelatorioconfiguracao": 248,
        "idrelatorioconsulta": 50,
        "idrelatorioconfiguracaoleiaute": 248,
        "idrelatoriousuarioleiaute": 1968,
        "ididioma": 1,
        "listaempresas": [3],
        "filtros": (
            "EquipeCRM=null;"
            "DesconsiderarEstornadoDevolvido=False;"
            "Cor=null;"
            "SemAutorizacaoExpedicao=True;"
            "ComAutorizacaoExpedicao=True;"
            "Tipodevenda=null;"
            "Periododamovimentacaofinal=2024-06-30 00:00;"
            "ComExpedicao=True;"
            "SemExpedicao=True;"
            "Modelodoveiculo=null;"
            "Tipodemovimento=2,9,11,17,21,25,26,32,10,22;"
            "Municipio=null;"
            "Consorcio=null;"
            "TipoVeiculo=null;"
            "Pessoa=null;"
            "Estadodoveiculo=null;"
            "Periododamovimentacaoinicial=2024-04-01 00:00;"
            "TipoPessoa=null;"
            "Pontodevendadovendedor=null;"
            "FinanceiraLeasing=null;"
            "FinanceiraCalculo=null;"
            "Origemdavenda=null;"
            "Vendedor=null;"
            "MovimentosCancelados=False"
        )
    }
    
    # Fazer a requisição e obter os dados de vendas
    vendas = make_request(body)
    # Criar um DataFrame para as vendas
    df_vendas = pd.DataFrame(vendas)
    
    # Filtrar os chassis do relatório pendente usando a coluna correta
    chassis_pendentes = relatorio_pendentes['CHASSI_VENDIDO'].tolist()

    # Verificar quais chassis do relatorio pendente não estão presentes nas vendas
    chassis_faltantes = [chassi for chassi in chassis_pendentes if chassi not in df_vendas['chassi'].tolist()]
    
    # Salvar os chassis faltantes em um arquivo de texto
    with open(output_faltantes_txt, 'w') as f:
        for chassi in chassis_faltantes:
            f.write(f"{chassi}\n")
    
    # Remover os chassis faltantes do DataFrame de pendentes
    pendentes_consolidados = relatorio_pendentes[~relatorio_pendentes['CHASSI_VENDIDO'].isin(chassis_faltantes)]

    #juntar as informacoes (chass com nome etc...)
    info_consolidado = pd.merge(pendentes_consolidados, pd.DataFrame(vendas), left_on='CHASSI_VENDIDO', right_on='chassi', how='left')
    info_consolidado = info_consolidado.drop(columns=['NOME_CLIENTE', 'TELEFONE_RESIDENCIAL', 'TELEFONE_COMERCIAL', 'RAMAL', 'E_MAIL'])

    #Filtrar por dias após a compra (DIAS_APOS_A_VENDA)

    # Periodo 1 - 23 a 29
    # Periodo 2 - 83 a 89
    # Periodo 3 - 153 a 159
    # Periodo 4 - 180 a 186

    # Filtrar por dias após a compra (DIAS_APOS_A_VENDA) baseado no tipo de disparo
    info_consolidado['DIAS_APOS_A_VENDA'] = pd.to_numeric(info_consolidado['DIAS_APOS_A_VENDA'], errors='coerce')
    if delta_D == 1:
        info_consolidado = info_consolidado[(info_consolidado['DIAS_APOS_A_VENDA'] >= 23) & (info_consolidado['DIAS_APOS_A_VENDA'] <= 29)]
    elif delta_D == 2:
        info_consolidado = info_consolidado[(info_consolidado['DIAS_APOS_A_VENDA'] >= 83) & (info_consolidado['DIAS_APOS_A_VENDA'] <= 89)]
    elif delta_D == 3:
        info_consolidado = info_consolidado[(info_consolidado['DIAS_APOS_A_VENDA'] >= 153) & (info_consolidado['DIAS_APOS_A_VENDA'] <= 159)]
    elif delta_D == 4:
        info_consolidado = info_consolidado[(info_consolidado['DIAS_APOS_A_VENDA'] >= 180) & (info_consolidado['DIAS_APOS_A_VENDA'] <= 186)]

    info_consolidado.to_excel(output_excel_consolidados)
    print(f"Dados salvos em {output_excel_consolidados}")

delta_D = int(input("Digite o tipo de disparo"))
processar_ihs(delta_D)
