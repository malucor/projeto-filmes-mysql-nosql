import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import crud_elenco, crud_filme

st.title("🎭 Gerenciar Elenco")
st.markdown("Nesta seção, é possível **adicionar** atores ao elenco de filmes, **atualizar** informações de protagonismo ou **remover** atores do elenco.")

tabela_placeholder = st.empty()


st.subheader("Adicionar Ator/Atriz a um Filme")
filme_data_ok, filmes = crud_filme.listar_filmes()
filme_opcoes = []
if filme_data_ok:
    for f in filmes:
        filme_opcoes.append(f"{f['num_filme']} - {f['nome']}")
if filme_opcoes:
    with st.form(key="form_adicionar_elenco"):
        filme_escolhido = st.selectbox("Filme:", filme_opcoes)
        ator_nome = st.text_input("Nome do Ator/Atriz")
        protagonista_flag = st.checkbox("Protagonista?")
        submit_add = st.form_submit_button("Adicionar")
    if submit_add:
        film_id = int(filme_escolhido.split(" - ")[0])
        success, msg = crud_elenco.adicionar_elenco(film_id, ator_nome, protagonista_flag)
        if success:
            st.success(msg)
        else:
            st.error(msg)
else:
    st.info("Cadastre pelo menos um filme antes de adicionar elenco.")


st.subheader("Atualizar Elenco (Protagonista)")
elenco_data_ok, elenco = crud_elenco.listar_elenco()
elenco_opcoes = []
if elenco_data_ok:
    for e in elenco:
        elenco_opcoes.append(f"{e['num_filme']} - {e['filme_nome']} | {e['nome_ator']}")
if elenco_opcoes:
    escolha = st.selectbox("Selecione o registro de elenco para editar:", elenco_opcoes)
    if escolha:
        partes = escolha.split(" | ")
        filme_part = partes[0]  
        ator_part = partes[1]   
        filme_id = int(filme_part.split(" - ")[0])
        ator_nome_sel = ator_part
        
        atual_protag = False
        for e in elenco:
            if e['num_filme'] == filme_id and e['nome_ator'] == ator_nome_sel:
                atual_protag = True if e['protagonista'] in [1, True] else False
                break
        with st.form(key="form_atualizar_elenco"):
            novo_protagonista = st.checkbox("Protagonista?", value=atual_protag)
            submit_update = st.form_submit_button("Atualizar")
        if submit_update:
            success, msg = crud_elenco.atualizar_elenco(filme_id, ator_nome_sel, novo_protagonista)
            if success:
                st.success(msg)
            else:
                st.error(msg)
else:
    st.info("Nenhum registro de elenco disponível para atualizar.")


st.subheader("Remover Ator/Atriz do Elenco")
if elenco_opcoes:
    with st.form(key="form_remover_elenco"):
        escolha_rem = st.selectbox("Selecione o registro de elenco para remover:", elenco_opcoes, key="elenco_del")
        submit_del = st.form_submit_button("Remover")
    if submit_del:
        partes = escolha_rem.split(" | ")
        filme_part = partes[0]
        ator_part = partes[1]
        filme_id = int(filme_part.split(" - ")[0])
        ator_nome_sel = ator_part
        success, msg = crud_elenco.remover_elenco(filme_id, ator_nome_sel)
        if success:
            st.success(msg)
        else:
            st.error(msg)
else:
    st.info("Nenhum registro de elenco disponível para remover.")


elenco_ok, elenco_data = crud_elenco.listar_elenco()
if elenco_ok:
    df = pd.DataFrame(elenco_data)
    df.columns = ["Código Filme", "Filme", "Ator/Atriz", "Protagonista"]
    df['Protagonista'] = df['Protagonista'].replace({0: 'Não', 1: 'Sim', False: 'Não', True: 'Sim'})
    tabela_placeholder.dataframe(df, use_container_width=True)
else:
    tabela_placeholder.error(elenco_data)
