import streamlit as st
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import crud_canal

st.title("📺 Gerenciar Canais")
st.markdown("Nesta seção, é possível **adicionar**, **editar** ou **remover** canais de TV.")


tabela_placeholder = st.empty()

st.subheader("Adicionar Canal")
with st.form(key="form_adicionar_canal"):
    novo_num = st.number_input("Número do canal", min_value=1, step=1)
    novo_nome = st.text_input("Nome do canal")
    submit_add = st.form_submit_button("Adicionar")
if submit_add:
    success, msg = crud_canal.adicionar_canal(int(novo_num), novo_nome)
    if success:
        st.success(msg)
    else:
        st.error(msg)


st.subheader("Atualizar Canal")

canal_opcoes = []
_selected_canal_id = None
canal_data_ok, canais = crud_canal.listar_canais()
if canal_data_ok:
    for c in canais:
        canal_opcoes.append(f"{c['num_canal']} - {c['nome']}")
if canal_opcoes:
    escolha = st.selectbox("Selecione o canal para editar:", canal_opcoes)
    if escolha:
    
        _selected_canal_id = int(escolha.split(" - ")[0])
        _selected_canal_nome = escolha.split(" - ")[1]
        with st.form(key="form_atualizar_canal"):
            novo_nome_canal = st.text_input("Novo nome do canal", value=_selected_canal_nome)
            submit_update = st.form_submit_button("Atualizar")
        if submit_update and _selected_canal_id is not None:
            success, msg = crud_canal.atualizar_canal(_selected_canal_id, novo_nome_canal)
            if success:
                st.success(msg)
            else:
                st.error(msg)
else:
    st.info("Nenhum canal cadastrado para atualizar.")


st.subheader("Remover Canal")
if canal_opcoes:
    with st.form(key="form_remover_canal"):
        escolha_del = st.selectbox("Selecione o canal para remover:", canal_opcoes, key="del")
        submit_del = st.form_submit_button("Remover")
    if submit_del:
        canal_id = int(escolha_del.split(" - ")[0])
        success, msg = crud_canal.remover_canal(canal_id)
        if success:
            st.success(msg)
        else:
            st.error(msg)
else:
    st.info("Nenhum canal cadastrado para remover.")

canais_ok, canais_data = crud_canal.listar_canais()
if canais_ok:
    df = pd.DataFrame(canais_data)
    df.columns = ["Número do Canal", "Nome"]
    tabela_placeholder.dataframe(df, use_container_width=True)
else:
    tabela_placeholder.error(canais_data)
