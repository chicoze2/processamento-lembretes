from db.connector import connect
from repo.Venda import Venda

import pandas as pd 

def main():
    ## Preparar os dados para serem inseridos no banco de dados
    ## Vendas - Chassi, Modelo, Nome, Contato (cel), Local, Data

    ## Abrir tabela Excel
    tabela_vendas = pd.read_excel('../planilhas/vendas.xlsx')  # Carregar a tabela Excel

    ## Ler a tabela Excel
    try: 
        vendas = []
        for index, row in tabela_vendas.iterrows():
            venda = Venda(row['Chassi'], row['Modelo'], row['Pessoa'], row['Celular'], row['Município UF'], row['Data Venda'])
            vendas.append(venda)
    except Exception as e:
        print(f"Erro ao processar a venda {index}: {e}")    

    ## Inserir os dados na tabela vendas
    try:
        conn = connect()  # Conectar ao banco de dados
        cursor = conn.cursor()
        
        for venda in vendas:
            ## "Limpar" a tabela Excel
            venda.padronizar_dados()
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

main()