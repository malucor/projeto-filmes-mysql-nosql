"""
Funções CRUD para a tabela Elenco.
"""
import mysql.connector
import db_connection

def adicionar_elenco(num_filme: int, nome_ator: str, protagonista: bool):
    """
    Insere um novo registro de elenco (ator em um filme).
    Retorna (True, mensagem_sucesso) ou (False, mensagem_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor()
    
        protagonista_bit = 1 if protagonista else 0
        cursor.execute(
            "INSERT INTO Elenco (num_filme, nome_ator, protagonista) VALUES (%s, %s, %s)",
            (num_filme, nome_ator, protagonista_bit)
        )
        conn.commit()
        return (True, f"Ator/atriz '{nome_ator}' adicionado(a) ao filme #{num_filme}.")
    except mysql.connector.Error as e:
        conn.rollback()
        if e.errno == 1062:
            return (False, "Erro: Este ator/atriz já está cadastrado(a) neste filme.")
        elif e.errno == 1452:
            return (False, "Erro: Filme associado não encontrado.")
        else:
            return (False, f"Erro ao adicionar elenco: {e.msg}")
    finally:
        conn.close()

def listar_elenco():
    """
    Retorna todos os registros de elenco, incluindo nome do filme.
    Em caso de sucesso, retorna (True, lista_elenco),
    onde cada item é um dicionário com num_filme, filme_nome, nome_ator, protagonista.
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor(dictionary=True)
       
        cursor.execute(
            "SELECT e.num_filme, f.nome AS filme_nome, e.nome_ator, e.protagonista "
            "FROM Elenco e JOIN Filme f ON e.num_filme = f.num_filme"
        )
        resultados = cursor.fetchall()
        return (True, resultados)
    except mysql.connector.Error as e:
        return (False, f"Erro ao listar elenco: {e.msg}")
    finally:
        conn.close()

def atualizar_elenco(num_filme: int, nome_ator: str, protagonista: bool):
    """
    Atualiza o status de protagonista de um ator em determinado filme.
    Retorna (True, mensagem_sucesso) ou (False, mensagem_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor()
        protagonista_bit = 1 if protagonista else 0
        cursor.execute(
            "UPDATE Elenco SET protagonista = %s WHERE num_filme = %s AND nome_ator = %s",
            (protagonista_bit, num_filme, nome_ator)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return (False, "Nenhum registro de elenco encontrado para atualizar.")
        return (True, f"Registro de elenco atualizado (Filme #{num_filme}, Ator '{nome_ator}').")
    except mysql.connector.Error as e:
        conn.rollback()
        return (False, f"Erro ao atualizar elenco: {e.msg}")
    finally:
        conn.close()

def remover_elenco(num_filme: int, nome_ator: str):
    """
    Remove um ator do elenco de um filme.
    Retorna (True, mensagem_sucesso) ou (False, mensagem_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Elenco WHERE num_filme = %s AND nome_ator = %s",
            (num_filme, nome_ator)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return (False, "Nenhum registro de elenco encontrado para remover.")
        return (True, f"Ator/atriz '{nome_ator}' removido(a) do filme #{num_filme}.")
    except mysql.connector.Error as e:
        conn.rollback()
        return (False, f"Erro ao remover do elenco: {e.msg}")
    finally:
        conn.close()
