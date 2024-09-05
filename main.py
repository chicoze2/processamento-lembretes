import pandas as pd

# Carregar o arquivo TXT
txt_file = 'relatorio.txt'

# Carregar dados TXT em DataFrame
data_txt = pd.read_csv(txt_file, sep='|')

# Carregar o arquivo Excel
excel_file = 'VENDAS.xlsx'
data_excel = pd.read_excel(excel_file)

# Supondo que o Excel também tenha uma coluna com o número do chassi para fazer o merge
# O nome da coluna deve ser ajustado conforme o nome real no arquivo Excel.
# Vamos supor que a coluna de chassi no Excel seja 'CHASSI_VENDIDO'
df_merged = pd.merge(data_txt, data_excel, on='Chassi', how='inner')

# Salvar a nova planilha com os dados combinados
df_merged.to_excel('/mnt/data/planilha_combinada.xlsx', index=False)

print("Planilha combinada criada com sucesso!")
