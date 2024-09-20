import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Obtém o caminho absoluto para o diretório atual (db)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Constrói o caminho para o arquivo .env na pasta src (um nível acima)
dotenv_path = os.path.join(current_dir, '..', '.env')
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path)

def connect():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        
        if conexao.is_connected():
            print('Conectado ao MySQL com sucesso!')
            return conexao
    
    except Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')
        return None

# Exemplo de uso
if __name__ == "__main__":
    conexao = connect()
    if conexao:
        # Faça suas operações no banco de dados aqui
        conexao.close()
        print('Conexão fechada.')
