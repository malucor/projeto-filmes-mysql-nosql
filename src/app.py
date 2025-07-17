import streamlit as st

# Configuração da página
st.set_page_config(page_title="Programação de Filmes", page_icon="🎬", layout="wide")

st.title("🎬 Programação de Filmes - Dashboard de Gerenciamento")
st.markdown("""
Bem-vindo à aplicação de **Programação de Filmes**. Esta interface permite realizar operações **CRUD** 
(com Criar, Ler, Atualizar, Deletar) em um banco de dados MySQL que gerencia canais de TV, filmes, elencos e exibições.
Use a **barra lateral** para navegar entre as seções:
- **Gerenciar Canais:** adicione novos canais, visualize, atualize ou remova canais existentes.
- **Gerenciar Filmes:** cadastre filmes, edite informações ou remova filmes do catálogo.
- **Gerenciar Elenco:** gerencie o elenco dos filmes (atores, atrizes e se são protagonistas).
- **Gerenciar Exibição:** agende filmes nos canais (datas e horários) e gerencie a programação.
- **Dashboard (Bônus):** visualize insights da programação, como contagem de exibições por canal.
""")
