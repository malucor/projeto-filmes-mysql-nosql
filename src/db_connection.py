"""
Módulo de conexão com o banco de dados MySQL.
Usa as credenciais seguras definidas em .streamlit/secrets.toml para estabelecer conexões.
Implementa um pool de conexões para eficiência e reutilização.
"""
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
import streamlit as st


_db_config = {
    "host": st.secrets["mysql"]["host"],
    "port": st.secrets["mysql"]["port"],
    "user": st.secrets["mysql"]["user"],
    "password": st.secrets["mysql"]["password"],
    "database": st.secrets["mysql"]["database"]
}


connection_pool = None
try:
    connection_pool = MySQLConnectionPool(pool_name="my_pool", pool_size=5, **_db_config)
except Exception as e:
    
    st.error(f"Erro ao conectar ao banco de dados: {e}")
    connection_pool = None

def get_connection():
    """
    Obtém uma conexão do pool de conexões.
    Importante: chame conn.close() após usar a conexão, para retorná-la ao pool.
    """
    global connection_pool
    if connection_pool is None:
        try:
            connection_pool = MySQLConnectionPool(pool_name="my_pool", pool_size=5, **_db_config)
        except Exception as e:
            st.error(f"Não foi possível conectar ao banco de dados: {e}")
            return None
    return connection_pool.get_connection()
