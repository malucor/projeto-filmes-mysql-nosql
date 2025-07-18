import streamlit as st
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import crud_elenco
import crud_filme # Para listar filmes

st.title("🎭 Gerenciar Elenco")
st.markdown("Nesta seção, é possível **adicionar**, **editar** o status de protagonista ou **remover** membros do elenco de filmes.")

tabela_placeholder = st.empty()


st.subheader("Adicionar Ator ao Elenco")
filmes_ok, filmes = crud_filme.listar_filmes()
filme_opcoes = ["Selecione um filme"]
filme_map = {}
if filmes_ok and filmes:
    for f in filmes:
        filme_opcoes.append(f"{f['num_filme']} - {f['nome']}")
        filme_map[f"{f['num_filme']} - {f['nome']}"] = f['num_filme']
else:
    st.warning("Nenhum filme cadastrado. Cadastre filmes antes de adicionar elenco.")


with st.form(key="form_adicionar_elenco"):
    filme_selecionado_str = st.selectbox("Filme:", options=filme_opcoes, key="add_filme_select")
    nome_ator = st.text_input("Nome do ator/atriz")
    protagonista = st.checkbox("É protagonista?")
    submit_add = st.form_submit_button("Adicionar")

if submit_add:
    if filme_selecionado_str == "Selecione um filme":
        st.error("Por favor, selecione um filme.")
    else:
        num_filme = filme_map[filme_selecionado_str]
        success, msg, sql_query = crud_elenco.adicionar_elenco(num_filme, nome_ator, protagonista)
        if success:
            st.success(msg)
        else:
            st.error(msg)
        if sql_query:
            st.code(sql_query, language="sql")

st.markdown("---")


st.subheader("Atualizar Status de Protagonista")
elenco_ok, elenco_atual = crud_elenco.listar_elenco()
elenco_opcoes = ["Selecione um ator/filme"]
elenco_map = {}

if elenco_ok and elenco_atual:
    for e in elenco_atual:
        opcao = f"{e['nome_filme']} - {e['nome_ator']}"
        elenco_opcoes.append(opcao)
        elenco_map[opcao] = {'num_filme': e['num_filme'], 'nome_ator': e['nome_ator'], 'protagonista': e['protagonista'], 'nome_filme': e['nome_filme']}
else:
    st.info("Nenhum elenco cadastrado para atualizar.")

if elenco_opcoes and len(elenco_opcoes) > 1:
    escolha_elenco_update = st.selectbox("Selecione o registro de elenco para editar:", options=elenco_opcoes, key="update_elenco_select")
    
    if escolha_elenco_update != "Selecione um ator/filme":
        selected_data = elenco_map[escolha_elenco_update]
        current_protagonista_status = selected_data['protagonista']
        
        with st.form(key="form_atualizar_protagonista"):
            novo_protagonista_status = st.checkbox("É protagonista?", value=current_protagonista_status)
            submit_update = st.form_submit_button("Atualizar Status")
        
        if submit_update:
            success, msg, sql_query = crud_elenco.atualizar_elenco(selected_data['num_filme'], selected_data['nome_ator'], novo_protagonista_status)
            if success:
                st.success(msg)
            else:
                st.error(msg)
            if sql_query:
                st.code(sql_query, language="sql")
else:
    if elenco_ok and not elenco_atual:
        st.info("Nenhum elenco cadastrado para atualizar.")
    elif not elenco_ok:
        st.error(elenco_atual)


st.subheader("Atualizar Nome do Ator")
if elenco_opcoes and len(elenco_opcoes) > 1:
    escolha_elenco_nome_update = st.selectbox("Selecione o ator para mudar o nome:", options=elenco_opcoes, key="update_actor_name_select")

    if escolha_elenco_nome_update != "Selecione um ator/filme":
        selected_data_name_update = elenco_map[escolha_elenco_nome_update]
        current_actor_name = selected_data_name_update['nome_ator']

        with st.form(key="form_atualizar_nome_ator"):
            st.write(f"Filme: **{selected_data_name_update['nome_filme']}** (Ator atual: **{current_actor_name}**)")
            novo_nome = st.text_input("Novo nome do ator/atriz", value=current_actor_name)
            submit_name_update = st.form_submit_button("Atualizar Nome")
        
        if submit_name_update:
            success, msg, sql_query = crud_elenco.atualizar_nome_ator(
                selected_data_name_update['num_filme'],
                current_actor_name,
                novo_nome
            )
            if success:
                st.success(msg)
            else:
                st.error(msg)
            if sql_query:
                st.code(sql_query, language="sql")
else:
    st.info("Nenhum elenco cadastrado para atualizar nomes de atores.")


st.subheader("Remover Ator do Elenco")
if elenco_opcoes and len(elenco_opcoes) > 1:
    with st.form(key="form_remover_elenco"):
        escolha_elenco_del = st.selectbox("Selecione o registro de elenco para remover:", options=elenco_opcoes, key="del_elenco_select")
        submit_del = st.form_submit_button("Remover")
    
    if submit_del:
        if escolha_elenco_del == "Selecione um ator/filme":
            st.error("Por favor, selecione um registro de elenco para remover.")
        else:
            selected_data = elenco_map[escolha_elenco_del]
            success, msg, sql_query = crud_elenco.remover_elenco(selected_data['num_filme'], selected_data['nome_ator'])
            if success:
                st.success(msg)
            else:
                st.error(msg)
            if sql_query:
                st.code(sql_query, language="sql")
else:
    if elenco_ok and not elenco_atual:
        st.info("Nenhum elenco cadastrado para remover.")
    elif not elenco_ok:
        st.error(elenco_atual)


# Exibir tabela de elenco
elenco_ok, elenco_data = crud_elenco.listar_elenco()
if elenco_ok:
    df = pd.DataFrame(elenco_data)
    df.columns = ["Cód. Filme", "Filme", "Ator/Atriz", "Protagonista"]
    df["Protagonista"] = df["Protagonista"].apply(lambda x: "Sim" if x else "Não")
    tabela_placeholder.dataframe(df, use_container_width=True)
else:
    tabela_placeholder.error(elenco_data)

st.markdown("---")
st.subheader("Demonstrar Violação de Integridade Referencial")
if st.button("Demonstrar Violação: Filme Inexistente para Elenco", key="btn_violacao_filme_elenco"):
    success, msg, sql_query = crud_elenco.adicionar_elenco(
        99999,
        "Ator Inexistente",
        False
    )
    if success:
        st.success(msg)
    else:
        st.error(f"Violação demonstrada: {msg}")
        if sql_query:
            st.code(sql_query, language="sql")