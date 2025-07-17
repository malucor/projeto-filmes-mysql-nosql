import streamlit as st
import pandas as pd
import sys, os
from datetime import date, time, datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import crud_exibicao
import crud_filme
import crud_canal

st.title("🗓️ Gerenciar Exibição")
st.markdown("Nesta seção, é possível **agendar**, **editar** ou **remover** exibições de filmes nos canais.")

tabela_placeholder = st.empty()


st.subheader("Agendar Nova Exibição")
# Obter lista de filmes e canais para seleção
filmes_ok, filmes = crud_filme.listar_filmes()
canais_ok, canais = crud_canal.listar_canais()

filme_opcoes = ["Selecione um filme"]
filme_map = {}
if filmes_ok and filmes:
    for f in filmes:
        filme_opcoes.append(f"{f['num_filme']} - {f['nome']}")
        filme_map[f"{f['num_filme']} - {f['nome']}"] = f['num_filme']

canal_opcoes = ["Selecione um canal"]
canal_map = {}
if canais_ok and canais:
    for c in canais:
        canal_opcoes.append(f"{c['num_canal']} - {c['nome']}")
        canal_map[f"{c['num_canal']} - {c['nome']}"] = c['num_canal']

if not (filmes_ok and filmes and canais_ok and canais):
    st.warning("É necessário ter filmes e canais cadastrados para agendar exibições.")

with st.form(key="form_adicionar_exibicao"):
    filme_selecionado_str = st.selectbox("Filme:", options=filme_opcoes, key="add_filme_select")
    canal_selecionado_str = st.selectbox("Canal:", options=canal_opcoes, key="add_canal_select")
    data_exibicao = st.date_input("Data da exibição", date.today())
    hora_exibicao = st.time_input("Hora da exibição", time(12, 0))
    submit_add = st.form_submit_button("Agendar Exibição")

if submit_add:
    if filme_selecionado_str == "Selecione um filme" or canal_selecionado_str == "Selecione um canal":
        st.error("Por favor, selecione um filme e um canal.")
    else:
        num_filme = filme_map[filme_selecionado_str]
        num_canal = canal_map[canal_selecionado_str]
        success, msg, sql_query = crud_exibicao.adicionar_exibicao(num_filme, num_canal, data_exibicao, hora_exibicao)
        if success:
            st.success(msg)
        else:
            st.error(msg)
        if sql_query:
            st.code(sql_query, language="sql")


st.subheader("Atualizar Exibição")
exibicoes_ok, exibicoes_data = crud_exibicao.listar_exibicoes()

exibicao_opcoes = ["Selecione uma exibição para atualizar"]
exibicao_map = {}

if exibicoes_ok and exibicoes_data:
    for e in exibicoes_data:
        if isinstance(e['hora_exibicao'], timedelta):
            total_seconds = int(e['hora_exibicao'].total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            display_time = time(hours, minutes, seconds)
        else:
            display_time = e['hora_exibicao']
        opcao = f"{e['nome_filme']} ({e['nome_canal']}) - {e['data_exibicao'].strftime('%d/%m/%Y')} {display_time.strftime('%H:%M')}"
        exibicao_opcoes.append(opcao)
        exibicao_map[opcao] = {
            'num_filme': e['num_filme'],
            'num_canal': e['num_canal'],
            'data_exibicao': e['data_exibicao'],
            'hora_exibicao': e['hora_exibicao']
        }
else:
    st.info("Nenhuma exibição cadastrada para atualizar.")

if exibicao_opcoes and len(exibicao_opcoes) > 1:
    escolha_exibicao_update = st.selectbox("Selecione a exibição:", options=exibicao_opcoes, key="update_exib_select")

    if escolha_exibicao_update != "Selecione uma exibição para atualizar":
        selected_data = exibicao_map[escolha_exibicao_update]
        
        current_hora_input_value = selected_data['hora_exibicao']
        if isinstance(current_hora_input_value, timedelta):
            total_seconds = int(current_hora_input_value.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            current_hora_input_value = time(hours, minutes, seconds)

        with st.form(key="form_atualizar_exibicao"):
            st.write(f"Atualizando exibição de **{escolha_exibicao_update.split(')')[0]})**")
            nova_data = st.date_input("Nova Data", value=selected_data['data_exibicao'])
            nova_hora = st.time_input("Nova Hora", value=current_hora_input_value)
            submit_update = st.form_submit_button("Atualizar")
        
        if submit_update:
            success, msg, sql_query = crud_exibicao.atualizar_exibicao(
                selected_data['num_filme'],
                selected_data['num_canal'],
                selected_data['data_exibicao'],
                selected_data['hora_exibicao'],
                nova_data,
                nova_hora
            )
            if success:
                st.success(msg)
            else:
                st.error(msg)
            if sql_query:
                st.code(sql_query, language="sql")
else:
    if exibicoes_ok and not exibicoes_data:
        st.info("Nenhuma exibição cadastrada para atualizar.")
    elif not exibicoes_ok:
        st.error(exibicoes_data)


st.subheader("Remover Exibição")
if exibicao_opcoes and len(exibicao_opcoes) > 1:
    with st.form(key="form_remover_exibicao"):
        escolha_exibicao_del = st.selectbox("Selecione a exibição para remover:", options=exibicao_opcoes, key="del_exib_select")
        submit_del = st.form_submit_button("Remover")
    
    if submit_del:
        if escolha_exibicao_del == "Selecione uma exibição para remover":
            st.error("Por favor, selecione uma exibição para remover.")
        else:
            selected_data = exibicao_map[escolha_exibicao_del]
            success, msg, sql_query = crud_exibicao.remover_exibicao(
                selected_data['num_filme'],
                selected_data['num_canal'],
                selected_data['data_exibicao'],
                selected_data['hora_exibicao']
            )
            if success:
                st.success(msg)
            else:
                st.error(msg)
            if sql_query:
                st.code(sql_query, language="sql")
else:
    if exibicoes_ok and not exibicoes_data:
        st.info("Nenhuma exibição cadastrada para remover.")
    elif not exibicoes_ok:
        st.error(exibicoes_data)


# Exibir tabela de exibições
exibicoes_ok, exibicoes_data_table = crud_exibicao.listar_exibicoes()
if exibicoes_ok:
    for row in exibicoes_data_table:
        if isinstance(row['hora_exibicao'], timedelta):
            total_seconds = int(row['hora_exibicao'].total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            row['hora_exibicao'] = time(hours, minutes, seconds)
            
    df = pd.DataFrame(exibicoes_data_table)
    df.columns = ["Cód. Filme", "Filme", "Cód. Canal", "Canal", "Data", "Hora"]
    tabela_placeholder.dataframe(df, use_container_width=True)
else:
    tabela_placeholder.error(exibicoes_data_table)