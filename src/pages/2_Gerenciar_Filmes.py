import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import crud_filme

st.title("🎞️ Gerenciar Filmes")
st.markdown("Nesta seção, é possível **adicionar**, **editar** ou **remover** filmes do catálogo.")

tabela_placeholder = st.empty()


st.subheader("Adicionar Filme")
with st.form(key="form_adicionar_filme"):
    novo_num = st.number_input("Código do filme", min_value=1, step=1)
    novo_nome = st.text_input("Nome do filme")
    novo_ano = st.number_input("Ano de lançamento", min_value=0, max_value=9999, step=1, value=0)
    novo_duracao = st.number_input("Duração (minutos)", min_value=0, step=1, value=0, help="Coloque 0 caso desconheça a duração.")
    submit_add = st.form_submit_button("Adicionar")
if submit_add:
    
    ano_val = int(novo_ano) if int(novo_ano) != 0 else None
    dur_val = int(novo_duracao) if int(novo_duracao) != 0 else None
    success, msg, sql_query = crud_filme.adicionar_filme(int(novo_num), novo_nome, ano_val, dur_val)
    if success:
        st.success(msg)
    else:
        st.error(msg)
    if sql_query:
        st.code(sql_query, language="sql")

st.subheader("Atualizar Filme")
filme_opcoes = []
_selected_filme_id = None
filme_data_ok, filmes = crud_filme.listar_filmes()
if filme_data_ok:
    for f in filmes:
        filme_opcoes.append(f"{f['num_filme']} - {f['nome']}")
if filme_opcoes:
    escolha = st.selectbox("Selecione o filme para editar:", filme_opcoes)
    if escolha:
        _selected_filme_id = int(escolha.split(" - ")[0])
     
        filme_atual = None
        for f in filmes:
            if f['num_filme'] == _selected_filme_id:
                filme_atual = f
                break
        if filme_atual:
            with st.form(key="form_atualizar_filme"):
                novo_nome_filme = st.text_input("Novo nome do filme", value=filme_atual['nome'])
                novo_ano_filme = st.number_input("Ano de lançamento", min_value=0, max_value=9999, step=1,
                                                 value=int(filme_atual['ano']) if filme_atual['ano'] is not None else 0)
                nova_duracao_filme = st.number_input("Duração (minutos)", min_value=0, step=1,
                                                     value=int(filme_atual['duracao']) if filme_atual['duracao'] is not None else 0)
                submit_update = st.form_submit_button("Atualizar")
            if submit_update:
                ano_val = int(novo_ano_filme) if int(novo_ano_filme) != 0 else None
                dur_val = int(nova_duracao_filme) if int(nova_duracao_filme) != 0 else None
                success, msg, sql_query = crud_filme.atualizar_filme(_selected_filme_id, novo_nome_filme, ano_val, dur_val)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
                if sql_query:
                    st.code(sql_query, language="sql")
else:
    st.info("Nenhum filme cadastrado para atualizar.")

st.subheader("Remover Filme")
if filme_opcoes:
    with st.form(key="form_remover_filme"):
        escolha_del = st.selectbox("Selecione o filme para remover:", filme_opcoes, key="filme_del")
        submit_del = st.form_submit_button("Remover")
    if submit_del:
        filme_id = int(escolha_del.split(" - ")[0])
        success, msg, sql_query = crud_filme.remover_filme(filme_id)
        if success:
            st.success(msg)
        else:
            st.error(msg)
        if sql_query:
            st.code(sql_query, language="sql")
else:
    st.info("Nenhum filme cadastrado para remover.")

filmes_ok, filmes_data = crud_filme.listar_filmes()
if filmes_ok:
    df = pd.DataFrame(filmes_data)
    df.columns = ["Código", "Nome", "Ano", "Duração (min)"]
    tabela_placeholder.dataframe(df, use_container_width=True)
else:
    tabela_placeholder.error(filmes_data)