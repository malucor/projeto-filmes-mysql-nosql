"""
Funções CRUD para a tabela Canal.
"""
import mysql.connector
import db_connection

def adicionar_canal(num_canal: int, nome: str):
    """
    Insere um novo canal na tabela Canal.
    Retorna (True, mensagem_sucesso) ou (False, mensagem_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Canal (num_canal, nome) VALUES (%s, %s)",
            (num_canal, nome)
        )
        conn.commit()
        return (True, f"Canal {nome} (#{num_canal}) adicionado com sucesso.")
    except mysql.connector.Error as e:
        conn.rollback()
        if e.errno == 1062:
            return (False, "Erro: Já existe um canal com esse número (chave duplicada).")
        else:
            return (False, f"Erro ao adicionar canal: {e.msg}")
    finally:
        conn.close()

def listar_canais():
    """
    Retorna todos os canais cadastrados.
    Em caso de sucesso, retorna (True, lista_de_canais),
    onde lista_de_canais é uma lista de dicionários com as colunas de Canal.
    Em caso de erro, retorna (False, mensagem_de_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT num_canal, nome FROM Canal")
        resultados = cursor.fetchall()
        return (True, resultados)
    except mysql.connector.Error as e:
        return (False, f"Erro ao listar canais: {e.msg}")
    finally:
        conn.close()

def atualizar_canal(num_canal: int, novo_nome: str):
    """
    Atualiza o nome de um canal existente.
    Retorna (True, mensagem_sucesso) ou (False, mensagem_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Canal SET nome = %s WHERE num_canal = %s",
            (novo_nome, num_canal)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return (False, "Nenhum canal encontrado com o número fornecido.")
        return (True, f"Canal #{num_canal} atualizado com sucesso.")
    except mysql.connector.Error as e:
        conn.rollback()
        return (False, f"Erro ao atualizar canal: {e.msg}")
    finally:
        conn.close()

def remover_canal(num_canal: int):
    """
    Remove um canal da tabela Canal.
    Retorna (True, mensagem_sucesso) ou (False, mensagem_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Canal WHERE num_canal = %s", (num_canal,))
        conn.commit()
        if cursor.rowcount == 0:
            return (False, "Nenhum canal encontrado com o número fornecido.")
        return (True, f"Canal #{num_canal} removido com sucesso.")
    except mysql.connector.Error as e:
        conn.rollback()
        if e.errno == 1451:
          
            return (False, "Não é possível remover este canal pois há exibições associadas a ele.")
        else:
            return (False, f"Erro ao remover canal: {e.msg}")
    finally:
        conn.close()
