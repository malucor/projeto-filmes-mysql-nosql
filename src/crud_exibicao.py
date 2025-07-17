"""
Funções CRUD para Exibicao (colunas data_exibicao, hora_exibicao).
"""
import mysql.connector
import db_connection

def adicionar_exibicao(num_filme: int, num_canal: int, data_exib: str, hora_exib: str):
    conn = db_connection.get_connection()
    if not conn:
        return False, "Falha na conexão."
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Exibicao (num_filme, num_canal, data_exibicao, hora_exibicao) "
            "VALUES (%s, %s, %s, %s)",
            (num_filme, num_canal, data_exib, hora_exib)
        )
        conn.commit()
        return True, "Exibição adicionada com sucesso."
    except mysql.connector.Error as e:
        conn.rollback()
        return False, f"Erro ao adicionar exibição: {e.msg}"
    finally:
        conn.close()

def listar_exibicoes():
    conn = db_connection.get_connection()
    if not conn:
        return False, "Falha na conexão."
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT e.num_filme, f.nome AS filme_nome, "
            "       e.num_canal, c.nome AS canal_nome, "
            "       e.data_exibicao, e.hora_exibicao "
            "FROM Exibicao e "
            "JOIN Filme f  ON e.num_filme = f.num_filme "
            "JOIN Canal c  ON e.num_canal = c.num_canal "
            "ORDER BY e.data_exibicao, e.hora_exibicao"
        )
        return True, cursor.fetchall()
    except mysql.connector.Error as e:
        return False, f"Erro ao listar exibições: {e.msg}"
    finally:
        conn.close()

def atualizar_exibicao(old_filme: int, old_canal: int, old_data: str, old_hora: str,
                       new_filme: int, new_canal: int, new_data: str, new_hora: str):
    conn = db_connection.get_connection()
    if not conn:
        return False, "Falha na conexão."
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Exibicao SET "
            "num_filme=%s, num_canal=%s, data_exibicao=%s, hora_exibicao=%s "
            "WHERE num_filme=%s AND num_canal=%s AND data_exibicao=%s AND hora_exibicao=%s",
            (new_filme, new_canal, new_data, new_hora,
             old_filme, old_canal, old_data, old_hora)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return False, "Nenhuma exibição encontrada para atualizar."
        return True, "Exibição atualizada com sucesso."
    except mysql.connector.Error as e:
        conn.rollback()
        return False, f"Erro ao atualizar exibição: {e.msg}"
    finally:
        conn.close()

def remover_exibicao(num_filme: int, num_canal: int, data_exib: str, hora_exib: str):
    conn = db_connection.get_connection()
    if not conn:
        return False, "Falha na conexão."
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Exibicao "
            "WHERE num_filme=%s AND num_canal=%s AND data_exibicao=%s AND hora_exibicao=%s",
            (num_filme, num_canal, data_exib, hora_exib)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return False, "Nenhuma exibição encontrada para remoção."
        return True, "Exibição removida com sucesso."
    except mysql.connector.Error as e:
        conn.rollback()
        return False, f"Erro ao remover exibição: {e.msg}"
    finally:
        conn.close()

def obter_contagem_exibicoes_por_canal():
    conn = db_connection.get_connection()
    if not conn:
        return False, "Falha na conexão."
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT c.nome, COUNT(*) "
            "FROM Exibicao e "
            "JOIN Canal c ON e.num_canal = c.num_canal "
            "GROUP BY c.nome"
        )
        return True, cursor.fetchall()
    except mysql.connector.Error as e:
        return False, f"Erro ao obter dados do dashboard: {e.msg}"
    finally:
        conn.close()
