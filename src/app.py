import os
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
- **Dashboard:** visualize queries e insights da programação.
""")

st.markdown("---")

st.subheader("Diagrama Entidade-Relacionamento (DER)")

image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrama_der.png')

if os.path.exists(image_path):
    st.image(image_path, caption="Melhor compreensão das tabelas e dos seus relacionamentos", use_container_width=False, width=500)
else:
    st.error(f"Erro: Imagem do DER não encontrada em: {image_path}. Certifique-se de que 'diagrama_der.png' está na pasta raiz do projeto.")

st.markdown("---")
