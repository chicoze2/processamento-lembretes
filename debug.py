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

# Realizar a junção dos DataFrames preservando todos os chassis do arquivo TXT
df_merged = pd.merge(data_txt, data_excel, left_on='CHASSI_VENDIDO', right_on='Chassi', how='left')

# Remover as colunas indesejadas
colunas_indesejadas = ['NOME_CLIENTE', 'TELEFONE_RESIDENCIAL', 'TELEFONE_COMERCIAL', 'RAMAL', 'E_MAIL']
df_merged.drop(columns=colunas_indesejadas, inplace=True, errors='ignore')

# Identificar chassis que estão no TXT mas não no Excel
chassis_nao_encontrados = df_merged[df_merged['Chassi'].isna()]

# Adicionar uma linha indicando os chassis não encontrados
if not chassis_nao_encontrados.empty:
  df_merged = pd.concat([df_merged, chassis_nao_encontrados])
  
# Salvar a nova planilha com os dados combinados, incluindo os chassis não encontrados
df_merged.to_excel('planilha_combinada.xlsx', index=False)


print("Planilha combinada criada com sucesso!")