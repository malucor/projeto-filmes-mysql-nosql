"""
Funções CRUD para a tabela Exibicao.
"""
import mysql.connector
import db_connection
from datetime import date, time, timedelta

def adicionar_exibicao(num_filme: int, num_canal: int, data_exibicao: date, hora_exibicao: time):
    """
    Insere uma nova exibição na tabela Exibicao.
    Retorna (True, mensagem_sucesso, sql_query) ou (False, mensagem_erro, sql_query).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None) 
    
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
        if e.errno == 1062: # Chave duplicada
            return (False, "Erro: Já existe uma exibição agendada para este filme/canal/data/hora.", sql_query)
        elif e.errno == 1452: # Falha de FK
            return (False, "Erro: O filme ou canal especificado não existe.", sql_query)
        else: # Outros erros
            return (False, f"Erro ao adicionar exibição: {e.msg}", sql_query)
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
            return (False, "Erro: Já existe uma exibição com a nova data/hora para este filme/canal.", sql_query)
        else:
            return (False, f"Erro ao atualizar exibição: {e.msg}", sql_query)
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
        return (False, f"Erro ao remover exibição: {e.msg}", sql_query)
    finally:
        conn.close()

def obter_contagem_exibicoes_por_canal():
    """
    Obtém a contagem de exibições por canal.
    Retorna (True, lista_de_resultados, sql_query) ou (False, mensagem_de_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    try:
        cursor = conn.cursor(dictionary=True)
        sql_query = """
            SELECT C.nome AS nome_canal, COUNT(E.num_filme) AS total_exibicoes
            FROM Exibicao E
            JOIN Canal C ON E.num_canal = C.num_canal
            GROUP BY C.num_canal, C.nome
            ORDER BY total_exibicoes DESC;
        """
        cursor.execute(sql_query)
        resultados = cursor.fetchall()
        return (True, resultados, sql_query)
    except mysql.connector.Error as e:
        return (False, f"Erro ao obter contagem de exibições por canal: {e.msg}", None)
    finally:
        conn.close()

def obter_contagem_exibicoes_por_horario():
    """
    Obtém a contagem de exibições por horário (apenas a hora).
    Retorna (True, lista_de_resultados, sql_query) ou (False, mensagem_de_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    try:
        cursor = conn.cursor(dictionary=True)
        sql_query = """
            SELECT HOUR(hora_exibicao) AS hora_do_dia, COUNT(*) AS total_exibicoes
            FROM Exibicao
            GROUP BY HOUR(hora_exibicao)
            ORDER BY hora_do_dia;
        """
        cursor.execute(sql_query)
        resultados = cursor.fetchall()
        return (True, resultados, sql_query)
    except mysql.connector.Error as e:
        return (False, f"Erro ao obter contagem de exibições por horário: {e.msg}", None)
    finally:
        conn.close()

def obter_exibicoes_por_dia_semana():
    """
    Obtém a contagem de exibições por dia da semana.
    Retorna (True, lista_de_resultados, sql_query) ou (False, mensagem_de_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    try:
        cursor = conn.cursor(dictionary=True)
        sql_query = """
            SELECT DAYOFWEEK(data_exibicao) AS dia_semana_num, COUNT(*) AS total_exibicoes
            FROM Exibicao
            GROUP BY dia_semana_num
            ORDER BY dia_semana_num;
        """
        cursor.execute(sql_query)
        resultados = cursor.fetchall()
        dias_semana_map = {
            1: 'Domingo', 2: 'Segunda-feira', 3: 'Terça-feira', 4: 'Quarta-feira',
            5: 'Quinta-feira', 6: 'Sexta-feira', 7: 'Sábado'
        }
        for row in resultados:
            row['dia_semana_nome'] = dias_semana_map.get(row['dia_semana_num'], 'Desconhecido')
        
        return (True, resultados, sql_query)
    except mysql.connector.Error as e:
        return (False, f"Erro ao obter contagem de exibições por dia da semana: {e.msg}", None)
    finally:
        conn.close()

def obter_filmes_com_exibicoes_futuras():
    """
    Obtém a lista de filmes com exibições agendadas a partir da data atual.
    Retorna (True, lista_de_resultados, sql_query) ou (False, mensagem_de_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    try:
        cursor = conn.cursor(dictionary=True)
        sql_query = """
            SELECT F.nome AS filme, C.nome AS canal, E.data_exibicao, E.hora_exibicao
            FROM Exibicao E
            JOIN Filme F ON E.num_filme = F.num_filme
            JOIN Canal C ON E.num_canal = C.num_canal
            WHERE E.data_exibicao >= CURDATE()
            ORDER BY E.data_exibicao, E.hora_exibicao;
        """
        cursor.execute(sql_query)
        resultados = cursor.fetchall()
        return (True, resultados, sql_query)
    except mysql.connector.Error as e:
        return (False, f"Erro ao obter filmes com exibições futuras: {e.msg}", None)
    finally:
        conn.close()

def obter_canais_sem_exibicoes_proximos_30_dias():
    """
    Obtém a lista de canais que não têm exibições agendadas nos próximos 30 dias.
    Retorna (True, lista_de_resultados, sql_query) ou (False, mensagem_de_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    try:
        cursor = conn.cursor(dictionary=True)
        sql_query = """
            SELECT C.nome AS canal_ocioso
            FROM Canal C
            LEFT JOIN Exibicao E ON C.num_canal = E.num_canal
            AND E.data_exibicao BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
            WHERE E.num_canal IS NULL;
        """
        cursor.execute(sql_query)
        resultados = cursor.fetchall()
        return (True, resultados, sql_query)
    except mysql.connector.Error as e:
        return (False, f"Erro ao obter canais sem exibições nos próximos 30 dias: {e.msg}", None)
    finally:
        conn.close()

def obter_canais_por_variedade_filmes():
    """
    Obtém a contagem de filmes únicos exibidos por cada canal.
    Retorna (True, lista_de_resultados, sql_query) ou (False, mensagem_de_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    try:
        cursor = conn.cursor(dictionary=True)
        sql_query = """
            SELECT C.nome AS nome_canal, COUNT(DISTINCT E.num_filme) AS quantidade_filmes_unicos
            FROM Exibicao E
            JOIN Canal C ON E.num_canal = C.num_canal
            GROUP BY C.nome
            ORDER BY quantidade_filmes_unicos DESC;
        """
        cursor.execute(sql_query)
        resultados = cursor.fetchall()
        return (True, resultados, sql_query)
    except mysql.connector.Error as e:
        return (False, f"Erro ao obter variedade de filmes por canal: {e.msg}", None)
    finally:
        conn.close()