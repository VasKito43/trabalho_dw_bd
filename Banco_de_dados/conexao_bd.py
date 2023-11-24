import psycopg2
import sqlite3


def get_conexao_postgres(banco_de_dados: str, usuario: str, senha: str, host: str = "localhost", porta: int = 5432):
    """
    Retorna uma conexão com o banco de dados PostgreSQL.

    Args:
        banco_de_dados (str): O nome do banco de dados ao qual você deseja se conectar.
        usuario (str): O nome de usuário utilizado para autenticação.
        senha (str): Senha utilizada para autenticação.
        host (str, optional): Endereço do servidor de banco de dados, por exemplo, localhost ou um endereço IP. Defaults to "localhost".
        porta (int, optional): O número da porta, que é 5432 por padrão se não for fornecido. Defaults to 5432.

    Returns:
        psycopg2.extensions.connection: Uma conexão com o banco de dados PostgreSQL.
    """
    conn = psycopg2.connect(
        host=host,
        database=banco_de_dados,
        user=usuario,
        password=senha,
        port=porta
    )
    return conn


def get_conexao_sqlite(bd_name: str = "bd_sqlite.db"):
    conn = sqlite3.connect(bd_name)
    return conn


def usa_conexao(conn):
    try:
        # cria um cursor
        cur = conn.cursor()
        # executa um statement
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except (Exception) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Conexao Fechada.')


def executa_comando(conn, comando: str):
    
    cur = conn.cursor()
    # executa um statement
    cur.execute(comando)
    db_version = cur.fetchone()
    print(db_version)
    cur.close()

    return db_version

def main():
    conn = get_conexao_postgres("sql_python", "postgres", "admin")
    print(f'Conexão do tipo {str(type(conn))} criada com sucesso!')
    db_version = executa_comando(conn, 'SELECT version()')
    print("Versão do PostgreSQL: ", db_version)
    conn.close()

    conn = get_conexao_sqlite()
    print(f'Conexão do tipo {str(type(conn))} criada com sucesso!')
    db_version = executa_comando(conn, 'SELECT SQLITE_VERSION()')
    print("Versão do SQLite: ", db_version)
    conn.close()


if __name__ == "__main__":
    main()
