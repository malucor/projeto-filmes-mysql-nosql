"""
Funções CRUD para a tabela Filme.
"""
import mysql.connector
import db_connection

def adicionar_filme(num_filme: int, nome: str, ano: int = None, duracao: int = None):
    """
    Insere um novo filme na tabela Filme.
    Retorna (True, mensagem_sucesso, sql_query) ou (False, mensagem_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    
    ano_for_db = ano if ano is not None else 0
    
    duracao_str = str(duracao) if duracao is not None else "NULL"
    sql_query = f"INSERT INTO Filme (num_filme, nome, ano, duracao) VALUES ({num_filme}, '{nome}', {ano_for_db}, {duracao_str})"
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Filme (num_filme, nome, ano, duracao) VALUES (%s, %s, %s, %s)",
            (num_filme, nome, ano_for_db, duracao)
        )
        conn.commit()
        return (True, f"Filme '{nome}' (#{num_filme}) adicionado com sucesso.", sql_query)
    except mysql.connector.Error as e:
        conn.rollback()
        if e.errno == 1062:
            return (False, "Erro: Já existe um filme com esse código (num_filme) cadastrado.", None)
        else:
            return (False, f"Erro ao adicionar filme: {e.msg}", sql_query)
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
    Retorna (True, mensagem_sucesso, sql_query) ou (False, mensagem_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
        
    novo_ano_for_db = novo_ano if novo_ano is not None else 0

    nova_duracao_str = str(nova_duracao) if nova_duracao is not None else "NULL"
    sql_query = f"UPDATE Filme SET nome = '{novo_nome}', ano = {novo_ano_for_db}, duracao = {nova_duracao_str} WHERE num_filme = {num_filme}"

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Filme SET nome = %s, ano = %s, duracao = %s WHERE num_filme = %s",
            (novo_nome, novo_ano_for_db, nova_duracao, num_filme)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return (False, "Nenhum filme encontrado com o código fornecido.", None)
        return (True, f"Filme #{num_filme} atualizado com sucesso.", sql_query)
    except mysql.connector.Error as e:
        conn.rollback()
        return (False, f"Erro ao atualizar filme: {e.msg}", sql_query)
    finally:
        conn.close()

def remover_filme(num_filme: int):
    """
    Remove um filme da tabela Filme.
    Retorna (True, mensagem_sucesso, sql_query) ou (False, mensagem_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
        
    sql_query = f"DELETE FROM Filme WHERE num_filme = {num_filme}"

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Filme WHERE num_filme = %s", (num_filme,))
        conn.commit()
        if cursor.rowcount == 0:
            return (False, "Nenhum filme encontrado com o código fornecido.", None)
        return (True, f"Filme #{num_filme} removido com sucesso.", sql_query)
    except mysql.connector.Error as e:
        conn.rollback()
        if e.errno == 1451:
            return (False, "Não é possível remover este filme pois há outros registros associados a ele (Elenco ou Exibição).", None)
        else:
            return (False, f"Erro ao remover filme: {e.msg}", sql_query)
    finally:
        conn.close()

def obter_media_duracao_filmes_por_ano():
    """
    Obtém a duração média dos filmes por ano de lançamento.
    Retorna (True, lista_de_resultados, sql_query) ou (False, mensagem_de_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    try:
        cursor = conn.cursor(dictionary=True)
        sql_query = """
            SELECT ano, AVG(duracao) AS media_duracao
            FROM Filme
            WHERE duracao IS NOT NULL
            GROUP BY ano
            ORDER BY ano;
        """
        cursor.execute(sql_query)
        resultados = cursor.fetchall()
        return (True, resultados, sql_query)
    except mysql.connector.Error as e:
        return (False, f"Erro ao obter média de duração de filmes por ano: {e.msg}", None)
    finally:
        conn.close()

def obter_quantidade_filmes_por_ano():
    """
    Obtém a quantidade de filmes lançados por ano.
    Retorna (True, lista_de_resultados, sql_query) ou (False, mensagem_de_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    try:
        cursor = conn.cursor(dictionary=True)
        sql_query = """
            SELECT ano, COUNT(*) AS total_filmes
            FROM Filme
            GROUP BY ano
            ORDER BY ano;
        """
        cursor.execute(sql_query)
        resultados = cursor.fetchall()
        return (True, resultados, sql_query)
    except mysql.connector.Error as e:
        return (False, f"Erro ao obter quantidade de filmes por ano: {e.msg}", None)
    finally:
        conn.close()

def obter_filmes_sem_exibicao():
    """
    Obtém uma lista de filmes que não possuem nenhuma exibição agendada.
    Retorna (True, lista_de_resultados, sql_query) ou (False, mensagem_de_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    try:
        cursor = conn.cursor(dictionary=True)
        sql_query = """
            SELECT F.nome AS filme_sem_exibicao, F.ano, F.duracao
            FROM Filme F
            LEFT JOIN Exibicao E ON F.num_filme = E.num_filme
            WHERE E.num_filme IS NULL
            ORDER BY F.nome;
        """
        cursor.execute(sql_query)
        resultados = cursor.fetchall()
        return (True, resultados, sql_query)
    except mysql.connector.Error as e:
        return (False, f"Erro ao obter filmes sem exibição: {e.msg}", None)
    finally:
        conn.close()

def obter_filmes_sem_elenco():
    """
    Obtém uma lista de filmes que não possuem nenhum ator no elenco.
    Retorna (True, lista_de_resultados, sql_query) ou (False, mensagem_de_erro, None).
    """
    conn = db_connection.get_connection()
    if conn is None:
        return (False, "Falha na conexão com o banco de dados.", None)
    try:
        cursor = conn.cursor(dictionary=True)
        sql_query = """
            SELECT F.nome AS filme_sem_elenco, F.ano, F.duracao
            FROM Filme F
            LEFT JOIN Elenco E ON F.num_filme = E.num_filme
            WHERE E.num_filme IS NULL
            ORDER BY F.nome;
        """
        cursor.execute(sql_query)
        resultados = cursor.fetchall()
        return (True, resultados, sql_query)
    except mysql.connector.Error as e:
        return (False, f"Erro ao obter filmes sem elenco: {e.msg}", None)
    finally:
        conn.close()