from db.connector import connect

def main():
    # Estabelece a conexão com o banco de dados
    conexao = connect()
    
    if conexao:
        try:
            # Cria um cursor para executar queries
            cursor = conexao.cursor()
            
            # Exemplo de query
            cursor.execute("SELECT VERSION()")
            
            # Recupera o resultado
            resultado = cursor.fetchone()
            
            # Imprime o resultado
            print(f"Versão do MySQL: {resultado[0]}")
            
        except Exception as e:
            print(f"Erro ao executar query: {e}")
        
        finally:
            # Fecha o cursor e a conexão
            if 'cursor' in locals():
                cursor.close()
            conexao.close()
            print("Conexão fechada.")
    else:
        print("Não foi possível conectar ao banco de dados.")
        return 0
    
    


if __name__ == "__main__":
    main()
