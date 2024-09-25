from db.connector import connect
from repo.Venda import Venda

import pandas as pd 

planilha_vendas = '../planilhas/vendas.xlsx'
relatorio_txt = '../planilhas/relatorio.txt'

def inserir_dados_vendas(planilha_vendas: str, relatorio_txt: str):
    ## Preparar os dados para serem inseridos no banco de dados
    ## Vendas - Chassi, Modelo, Nome, Contato (cel), Local, Data

    ## Abrir os dados do relatorio de revisoes pendentes no IHS.
    data_txt = pd.read_csv(relatorio_txt, sep='|')
    ## Abrir tabela Excel
    tabela_vendas = pd.read_excel(planilha_vendas)  # Carregar a tabela Excel

    # Juntar os dados do relatorio com a tabela de vendas (considerar todos os chassis do relatorio)
    vendas = pd.merge(data_txt, tabela_vendas, left_on='CHASSI_VENDIDO', right_on='Chassi', how='left')

    # Identificar chassis que estão no TXT mas não no Excel
    chassis_nao_encontrados = vendas[vendas['Chassi'].isna()]

    # Remover chassis não encontrados da tabela de vendas
    vendas = vendas.dropna(subset=['Chassi'])

    # Salvar apenas os chassis não encontrados em um arquivo TXT
    chassis_nao_encontrados['CHASSI_VENDIDO'].to_csv('chassis_nao_encontrados.txt', index=False, header=False)
    # Processar apenas os chassis encontrados
    try: 
        vendas = vendas.sort_values(by='Pessoa')
        vendas_list = []
        for index, row in vendas.iterrows():
            venda = Venda(row['Chassi'], row['Modelo'], row['Pessoa'], row['Celular'], row['Município UF'], row['Data Venda'])
            vendas_list.append(venda)
    except Exception as e:
        print(f"Erro ao processar a venda {index}: {e}")    
    
    try:
        conn = connect()  # Conectar ao banco de dados
        cursor = conn.cursor()
        
        for venda in vendas_list:
            ## "Limpar" a tabela Excel
            venda.padronizar_dados()
            ## Inserir os dados na tabela vendas
            cursor.execute(
                "INSERT INTO Vendas (chassi, modelo, nome, contato, local, data_venda) VALUES (%s, %s, %s, %s, %s, %s)",
                (venda.chassi, venda.modelo, venda.nome, venda.contato, venda.local, venda.data)
            )
            conn.commit()
            print(f"Venda inserida: {venda}")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao inserir a venda {venda}: {e}")

inserir_dados_vendas(planilha_vendas, relatorio_txt)