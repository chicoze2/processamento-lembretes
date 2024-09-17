import pandas as pd

# Carregar o arquivo TXT
txt_file = 'relatorio.txt'
data_txt = pd.read_csv(txt_file, sep='|')

# Carregar o arquivo Excel
excel_file = 'VENDAS.xlsx'
data_excel = pd.read_excel(excel_file)

# Exibir colunas dos DataFrames para verificar os nomes
print("Colunas no arquivo TXT:", data_txt.columns)
print("Colunas no arquivo Excel:", data_excel.columns)

# Verifique o nome correto da coluna de chassi em ambos os DataFrames e ajuste aqui
# Exemplo: Se a coluna no Excel for chamada de 'Chassi', mas no TXT for 'CHASSI_VENDIDO'
df_merged = pd.merge(data_txt, data_excel, left_on='CHASSI_VENDIDO', right_on='Chassi', how='left')

# Salvar a nova planilha com os dados combinados
df_merged.to_excel('planilha_combinada.xlsx', index=False)

print("Planilha combinada criada com sucesso!")
