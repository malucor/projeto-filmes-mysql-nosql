import streamlit as st
import pandas as pd
import datetime
import sys, os

# Permite importar módulos da pasta pai (crud_*).
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import crud_exibicao, crud_filme, crud_canal


st.title("📅 Gerenciar Exibições")
tabela_placeholder = st.empty()  

filmes_ok, filmes = crud_filme.listar_filmes()
canais_ok, canais = crud_canal.listar_canais()

filme_opts = [f"{f['num_filme']} - {f['nome']}" for f in filmes] if filmes_ok else []
canal_opts = [f"{c['num_canal']} - {c['nome']}" for c in canais] if canais_ok else []

st.subheader("Agendar Exibição")
if not filme_opts or not canal_opts:
    st.info("Cadastre pelo menos **um filme** e **um canal** antes de agendar exibições.")
else:
    with st.form("form_add"):
        filme_sel = st.selectbox("Filme", filme_opts)
        canal_sel = st.selectbox("Canal", canal_opts)
        data_sel  = st.date_input("Data", value=datetime.date.today())
        hora_sel  = st.time_input("Hora", value=datetime.time(0, 0))
        if st.form_submit_button("Agendar"):
            film_id  = int(filme_sel.split(" - ")[0])
            canal_id = int(canal_sel.split(" - ")[0])
            ok, msg  = crud_exibicao.adicionar_exibicao(
                film_id,
                canal_id,
                data_sel.strftime("%Y-%m-%d"),
                hora_sel.strftime("%H:%M:%S")
            )
            if ok:
                st.success(msg)
            else:
                st.error(msg)

ok_exib, exibicoes = crud_exibicao.listar_exibicoes()
exib_opts = [
    f"{e['num_filme']}|{e['num_canal']}|{e['data_exibicao']}|{e['hora_exibicao']} - "
    f"{e['filme_nome']} • {e['data_exibicao']} {e['hora_exibicao']} • Canal {e['canal_nome']}"
    for e in exibicoes
] if ok_exib else []


st.subheader("Atualizar Exibição")
if not exib_opts:
    st.info("Nenhuma exibição cadastrada para atualizar.")
else:
    with st.form("form_update"):
        escolha = st.selectbox("Selecione a exibição", exib_opts)
     
        old_film, old_canal, old_data, old_hora = escolha.split(" - ")[0].split("|")
        old_date_dt = datetime.datetime.strptime(old_data, "%Y-%m-%d").date()
        old_time_dt = datetime.datetime.strptime(old_hora, "%H:%M:%S").time()

 
        filme_novo = st.selectbox(
            "Novo Filme", filme_opts,
            index=[i for i, o in enumerate(filme_opts) if o.startswith(f"{old_film} ")][0]
        )
        canal_novo = st.selectbox(
            "Novo Canal", canal_opts,
            index=[i for i, o in enumerate(canal_opts) if o.startswith(f"{old_canal} ")][0]
        )
        data_nova = st.date_input("Nova Data", value=old_date_dt)
        hora_nova = st.time_input("Nova Hora", value=old_time_dt)

        if st.form_submit_button("Atualizar"):
            ok_upd, msg_upd = crud_exibicao.atualizar_exibicao(
                int(old_film), int(old_canal), old_data, old_hora,
                int(filme_novo.split(" - ")[0]),
                int(canal_novo.split(" - ")[0]),
                data_nova.strftime("%Y-%m-%d"),
                hora_nova.strftime("%H:%M:%S")
            )
            if ok_upd:
                st.success(msg_upd)
            else:
                st.error(msg_upd)


st.subheader("Remover Exibição")
if not exib_opts:
    st.info("Nenhuma exibição cadastrada para remover.")
else:
    with st.form("form_delete"):
        escolha_del = st.selectbox("Selecione a exibição", exib_opts, key="del")
        if st.form_submit_button("Remover"):
            film_del, canal_del, data_del, hora_del = escolha_del.split(" - ")[0].split("|")
            ok_del, msg_del = crud_exibicao.remover_exibicao(
                int(film_del), int(canal_del), data_del, hora_del
            )
            if ok_del:
                st.success(msg_del)
            else:
                st.error(msg_del)

if ok_exib and len(exibicoes) > 0:
    df = pd.DataFrame(exibicoes)
    df.columns = ["FilmeID", "Filme", "CanalID", "Canal", "Data", "Hora"]
    tabela_placeholder.dataframe(df, use_container_width=True)
elif ok_exib:
    tabela_placeholder.info("Nenhuma exibição cadastrada no momento.")
else:
    tabela_placeholder.error(exibicoes)  
