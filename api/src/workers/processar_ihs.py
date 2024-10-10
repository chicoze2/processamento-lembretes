import pandas as pd
from connect import make_request

relatorio_txt = 'api/src/workers/taubate_maio.txt'
output_faltantes_txt = 'chassis_faltantes.txt'
output_excel_consolidados = 'pendentes_consolidados.xlsx'

def processar_ihs():
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
            "Periododamovimentacaofinal=2024-05-31 00:00;"
            "ComExpedicao=True;"
            "SemExpedicao=True;"
            "Modelodoveiculo=null;"
            "Tipodemovimento=2,9,11,17,21,25,26,32,10,22;"
            "Municipio=null;"
            "Consorcio=null;"
            "TipoVeiculo=null;"
            "Pessoa=null;"
            "Estadodoveiculo=null;"
            "Periododamovimentacaoinicial=2024-05-01 00:00;"
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
    info_consolidado.to_excel("infos_consolidado.xlsx")

    print(info_consolidado)
processar_ihs()
