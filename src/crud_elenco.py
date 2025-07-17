"""
Funções CRUD para a tabela Elenco.
"""
import mysql.connector
import db_connection

def adicionar_elenco(num_filme: int, nome_ator: str, protagonista: bool):
    """
    Insere um novo ator ao elenco de um filme na tabela Elenco.
    Retorna (True, mensagem_sucesso, sql_query) ou (False, mensagem_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    
    protagonista_sql = 1 if protagonista else 0
    sql_query = f"INSERT INTO Elenco (num_filme, nome_ator, protagonista) VALUES ({num_filme}, '{nome_ator}', {protagonista_sql})"
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Elenco (num_filme, nome_ator, protagonista) VALUES (%s, %s, %s)",
            (num_filme, nome_ator, protagonista)
        )
        conn.commit()
        return (True, f"Ator '{nome_ator}' adicionado ao filme #{num_filme} com sucesso.", sql_query)
    except mysql.connector.Error as e:
        conn.rollback()
        if e.errno == 1062: # Duplicate entry for primary key
            return (False, "Erro: Este ator já faz parte do elenco deste filme.", None)
        elif e.errno == 1452: # Foreign key constraint fails
            return (False, "Erro: O filme especificado não existe.", None)
        else:
            return (False, f"Erro ao adicionar elenco: {e.msg}", None)
    finally:
        conn.close()

def listar_elenco():
    """
    Retorna todos os registros de elenco cadastrados.
    Em caso de sucesso, retorna (True, lista_de_elenco),
    onde cada item é um dicionário com campos num_filme, nome_ator, protagonista.
    Em caso de erro, retorna (False, mensagem_de_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT E.num_filme, F.nome AS nome_filme, E.nome_ator, E.protagonista
            FROM Elenco E
            JOIN Filme F ON E.num_filme = F.num_filme
            ORDER BY F.nome, E.protagonista DESC, E.nome_ator
        """)
        resultados = cursor.fetchall()
        return (True, resultados)
    except mysql.connector.Error as e:
        return (False, f"Erro ao listar elenco: {e.msg}")
    finally:
        conn.close()

def atualizar_elenco(num_filme: int, nome_ator: str, novo_protagonista: bool):
    """
    Atualiza o status de protagonista de um ator no elenco de um filme.
    Retorna (True, mensagem_sucesso, sql_query) ou (False, mensagem_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)

    novo_protagonista_sql = 1 if novo_protagonista else 0
    sql_query = f"UPDATE Elenco SET protagonista = {novo_protagonista_sql} WHERE num_filme = {num_filme} AND nome_ator = '{nome_ator}'"

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Elenco SET protagonista = %s WHERE num_filme = %s AND nome_ator = %s",
            (novo_protagonista, num_filme, nome_ator)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return (False, "Nenhum registro de elenco encontrado com os dados fornecidos.", None)
        return (True, f"Status de protagonista de '{nome_ator}' no filme #{num_filme} atualizado com sucesso.", sql_query)
    except mysql.connector.Error as e:
        conn.rollback()
        return (False, f"Erro ao atualizar elenco: {e.msg}", None)
    finally:
        conn.close()

def remover_elenco(num_filme: int, nome_ator: str):
    """
    Remove um ator do elenco de um filme da tabela Elenco.
    Retorna (True, mensagem_sucesso, sql_query) ou (False, mensagem_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
        
    sql_query = f"DELETE FROM Elenco WHERE num_filme = {num_filme} AND nome_ator = '{nome_ator}'"

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Elenco WHERE num_filme = %s AND nome_ator = %s", (num_filme, nome_ator))
        conn.commit()
        if cursor.rowcount == 0:
            return (False, "Nenhum registro de elenco encontrado com os dados fornecidos.", None)
        return (True, f"Ator '{nome_ator}' removido do filme #{num_filme} com sucesso.", sql_query)
    except mysql.connector.Error as e:
        conn.rollback()
        return (False, f"Erro ao remover elenco: {e.msg}", None)
    finally:
        conn.close()