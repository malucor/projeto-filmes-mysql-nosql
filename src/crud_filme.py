"""
Funções CRUD para a tabela Filme.
"""
import mysql.connector
import db_connection

def adicionar_filme(num_filme: int, nome: str, ano: int = None, duracao: int = None):
    """
    Insere um novo filme na tabela Filme.
    Retorna (True, mensagem_sucesso) ou (False, mensagem_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Filme (num_filme, nome, ano, duracao) VALUES (%s, %s, %s, %s)",
            (num_filme, nome, ano, duracao)
        )
        conn.commit()
        return (True, f"Filme '{nome}' (#{num_filme}) adicionado com sucesso.")
    except mysql.connector.Error as e:
        conn.rollback()
        if e.errno == 1062:
            return (False, "Erro: Já existe um filme com esse código (num_filme) cadastrado.")
        else:
            return (False, f"Erro ao adicionar filme: {e.msg}")
    finally:
        conn.close()

def listar_filmes():
    """
    Retorna todos os filmes cadastrados.
    Em caso de sucesso, retorna (True, lista_de_filmes),
    onde cada filme é um dicionário com campos num_filme, nome, ano, duracao.
    Em caso de erro, retorna (False, mensagem_de_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT num_filme, nome, ano, duracao FROM Filme")
        resultados = cursor.fetchall()
        return (True, resultados)
    except mysql.connector.Error as e:
        return (False, f"Erro ao listar filmes: {e.msg}")
    finally:
        conn.close()

def atualizar_filme(num_filme: int, novo_nome: str, novo_ano: int = None, nova_duracao: int = None):
    """
    Atualiza os dados de um filme existente (nome, ano, duração).
    Retorna (True, mensagem_sucesso) ou (False, mensagem_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Filme SET nome = %s, ano = %s, duracao = %s WHERE num_filme = %s",
            (novo_nome, novo_ano, nova_duracao, num_filme)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return (False, "Nenhum filme encontrado com o código fornecido.")
        return (True, f"Filme #{num_filme} atualizado com sucesso.")
    except mysql.connector.Error as e:
        conn.rollback()
        return (False, f"Erro ao atualizar filme: {e.msg}")
    finally:
        conn.close()

def remover_filme(num_filme: int):
    """
    Remove um filme da tabela Filme.
    Retorna (True, mensagem_sucesso) ou (False, mensagem_erro).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Filme WHERE num_filme = %s", (num_filme,))
        conn.commit()
        if cursor.rowcount == 0:
            return (False, "Nenhum filme encontrado com o código fornecido.")
        return (True, f"Filme #{num_filme} removido com sucesso.")
    except mysql.connector.Error as e:
        conn.rollback()
        if e.errno == 1451:
            
            return (False, "Não é possível remover este filme pois há outros registros associados a ele (Elenco ou Exibição).")
        else:
            return (False, f"Erro ao remover filme: {e.msg}")
    finally:
        conn.close()
