"""
Funções CRUD para a tabela Exibicao.
"""
import mysql.connector
import db_connection
from datetime import date, time

def adicionar_exibicao(num_filme: int, num_canal: int, data_exibicao: date, hora_exibicao: time):
    """
    Insere uma nova exibição na tabela Exibicao.
    Retorna (True, mensagem_sucesso, sql_query) ou (False, mensagem_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    
    # SQL para exibição
    sql_query = f"INSERT INTO Exibicao (num_filme, num_canal, data_exibicao, hora_exibicao) VALUES ({num_filme}, {num_canal}, '{data_exibicao}', '{hora_exibicao}')"
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Exibicao (num_filme, num_canal, data_exibicao, hora_exibicao) VALUES (%s, %s, %s, %s)",
            (num_filme, num_canal, data_exibicao, hora_exibicao)
        )
        conn.commit()
        return (True, f"Exibição agendada para o filme #{num_filme} no canal #{num_canal} em {data_exibicao} às {hora_exibicao} com sucesso.", sql_query)
    except mysql.connector.Error as e:
        conn.rollback()
        if e.errno == 1062: # Duplicate entry for primary key
            return (False, "Erro: Já existe uma exibição agendada para este filme/canal/data/hora.", None)
        elif e.errno == 1452: # Foreign key constraint fails
            return (False, "Erro: O filme ou canal especificado não existe.", None)
        else:
            return (False, f"Erro ao adicionar exibição: {e.msg}", None)
    finally:
        conn.close()

def listar_exibicoes():
    """
    Retorna todas as exibições cadastradas.
    Em caso de sucesso, retorna (True, lista_de_exibicoes),
    onde cada exibição é um dicionário com campos num_filme, nome_filme, num_canal, nome_canal, data_exibicao, hora_exibicao.
    Em caso de erro, retorna (False, mensagem_de_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT E.num_filme, F.nome AS nome_filme, E.num_canal, C.nome AS nome_canal, E.data_exibicao, E.hora_exibicao
            FROM Exibicao E
            JOIN Filme F ON E.num_filme = F.num_filme
            JOIN Canal C ON E.num_canal = C.num_canal
            ORDER BY E.data_exibicao DESC, E.hora_exibicao DESC
        """)
        resultados = cursor.fetchall()
        return (True, resultados)
    except mysql.connector.Error as e:
        return (False, f"Erro ao listar exibições: {e.msg}")
    finally:
        conn.close()

def atualizar_exibicao(num_filme: int, num_canal: int, data_exibicao: date, hora_exibicao: time,
                       nova_data_exibicao: date, nova_hora_exibicao: time):
    """
    Atualiza a data e/ou hora de uma exibição existente.
    Retorna (True, mensagem_sucesso, sql_query) ou (False, mensagem_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)

    # SQL para exibição
    sql_query = f"UPDATE Exibicao SET data_exibicao = '{nova_data_exibicao}', hora_exibicao = '{nova_hora_exibicao}' WHERE num_filme = {num_filme} AND num_canal = {num_canal} AND data_exibicao = '{data_exibicao}' AND hora_exibicao = '{hora_exibicao}'"

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Exibicao
            SET data_exibicao = %s, hora_exibicao = %s
            WHERE num_filme = %s AND num_canal = %s AND data_exibicao = %s AND hora_exibicao = %s
            """,
            (nova_data_exibicao, nova_hora_exibicao, num_filme, num_canal, data_exibicao, hora_exibicao)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return (False, "Nenhum agendamento de exibição encontrado com os dados fornecidos.", None)
        return (True, f"Exibição do filme #{num_filme} no canal #{num_canal} atualizada com sucesso.", sql_query)
    except mysql.connector.Error as e:
        conn.rollback()
        if e.errno == 1062: # Duplicate entry for primary key
            return (False, "Erro: Já existe uma exibição com a nova data/hora para este filme/canal.", None)
        else:
            return (False, f"Erro ao atualizar exibição: {e.msg}", None)
    finally:
        conn.close()

def remover_exibicao(num_filme: int, num_canal: int, data_exibicao: date, hora_exibicao: time):
    """
    Remove uma exibição da tabela Exibicao.
    Retorna (True, mensagem_sucesso, sql_query) ou (False, mensagem_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
        
    sql_query = f"DELETE FROM Exibicao WHERE num_filme = {num_filme} AND num_canal = {num_canal} AND data_exibicao = '{data_exibicao}' AND hora_exibicao = '{hora_exibicao}'"

    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Exibicao WHERE num_filme = %s AND num_canal = %s AND data_exibicao = %s AND hora_exibicao = %s",
            (num_filme, num_canal, data_exibicao, hora_exibicao)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return (False, "Nenhum agendamento de exibição encontrado com os dados fornecidos.", None)
        return (True, f"Exibição do filme #{num_filme} no canal #{num_canal} removida com sucesso.", sql_query)
    except mysql.connector.Error as e:
        conn.rollback()
        return (False, f"Erro ao remover exibição: {e.msg}", None)
    finally:
        conn.close()