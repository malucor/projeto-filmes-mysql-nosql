import streamlit as st
import pandas as pd
import sys, os
from datetime import time, timedelta, date
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import crud_exibicao
import crud_elenco
import crud_filme

if 'show_query_canal' not in st.session_state:
    st.session_state.show_query_canal = False
if 'show_query_hora' not in st.session_state:
    st.session_state.show_query_hora = False
if 'show_query_dia_semana' not in st.session_state:
    st.session_state.show_query_dia_semana = False
if 'show_query_media_duracao' not in st.session_state:
    st.session_state.show_query_media_duracao = False
if 'show_query_filmes_sem_exibicao' not in st.session_state:
    st.session_state.show_query_filmes_sem_exibicao = False
if 'show_query_filmes_sem_elenco' not in st.session_state: # NOVA
    st.session_state.show_query_filmes_sem_elenco = False
if 'show_query_filmes_futuros' not in st.session_state:
    st.session_state.show_query_filmes_futuros = False
if 'show_query_multi_ator' not in st.session_state:
    st.session_state.show_query_multi_ator = False
if 'show_query_proto_multi_ator' not in st.session_state:
    st.session_state.show_query_proto_multi_ator = False
if 'show_query_ator_sem_proto' not in st.session_state:
    st.session_state.show_query_ator_sem_proto = False
if 'show_query_canais_variedade' not in st.session_state:
    st.session_state.show_query_canais_variedade = False
if 'show_query_canais_ociosos' not in st.session_state:
    st.session_state.show_query_canais_ociosos = False


st.title("📊 Dashboard de Exibições")
st.markdown("Esta seção apresenta um **gráfico** com insights sobre a programação de filmes, elencos e canais, com base nos dados atuais.")

st.header("🎥 Visão Geral da Programação")
st.markdown("---")

st.subheader("Exibições por Canal")
ok_canal, resultado_canal, query_canal = crud_exibicao.obter_contagem_exibicoes_por_canal()
if ok_canal:
    if resultado_canal:
        df_canal = pd.DataFrame(resultado_canal)
        df_canal = df_canal.rename(columns={'nome_canal': 'Canal', 'total_exibicoes': 'Total de Exibições'})
        
        fig_canal = px.bar(df_canal, x="Canal", y="Total de Exibições", 
                           labels={"Total de Exibições": "Quantidade de Exibições"})
        st.plotly_chart(fig_canal, use_container_width=True)

        st.table(df_canal.set_index("Canal"))
        
        if st.button("Visualizar Query", key="btn_query_canal"):
            st.session_state.show_query_canal = not st.session_state.show_query_canal
        
        if st.session_state.show_query_canal:
            st.markdown("```sql\n" + query_canal + "\n```")
    else:
        st.info("Nenhuma exibição encontrada para gerar o dashboard de canais.")
else:
    st.error(resultado_canal)

st.markdown("---")

st.subheader("Exibições por Horário")
ok_hora, resultado_hora, query_hora = crud_exibicao.obter_contagem_exibicoes_por_horario()

if ok_hora:
    if resultado_hora:
        for row in resultado_hora:
            row['hora_do_dia'] = f"{row['hora_do_dia']:02d}"
            
        df_hora = pd.DataFrame(resultado_hora)
        df_hora = df_hora.rename(columns={'hora_do_dia': 'Horário', 'total_exibicoes': 'Total de Exibições'})

        fig_hora = px.bar(df_hora, x="Horário", y="Total de Exibições", 
                          labels={"Total de Exibições": "Quantidade de Exibições"})
        fig_hora.update_xaxes(categoryorder='category ascending')
        st.plotly_chart(fig_hora, use_container_width=True)

        st.table(df_hora.set_index("Horário"))
        
        if st.button("Visualizar Query", key="btn_query_hora"):
            st.session_state.show_query_hora = not st.session_state.show_query_hora

        if st.session_state.show_query_hora:
            st.markdown("```sql\n" + query_hora + "\n```")
    else:
        st.info("Nenhuma exibição encontrada para gerar o dashboard de horários.")
else:
    st.error(resultado_hora)

st.markdown("---")

st.subheader("Exibições por Dia da Semana")
ok_dia_semana, resultado_dia_semana, query_dia_semana = crud_exibicao.obter_exibicoes_por_dia_semana()

if ok_dia_semana:
    if resultado_dia_semana:
        df_dia_semana = pd.DataFrame(resultado_dia_semana)
        dias_ordem = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']
        df_dia_semana['dia_semana_nome'] = pd.Categorical(df_dia_semana['dia_semana_nome'], categories=dias_ordem, ordered=True)
        df_dia_semana = df_dia_semana.sort_values('dia_semana_nome')

        df_dia_semana = df_dia_semana.rename(columns={'dia_semana_nome': 'Dia da Semana', 'total_exibicoes': 'Total de Exibições'})
        
        fig_dia_semana = px.bar(df_dia_semana, x="Dia da Semana", y="Total de Exibições",
                                labels={"Total de Exibições": "Quantidade de Exibições"})
        st.plotly_chart(fig_dia_semana, use_container_width=True)
        
        st.table(df_dia_semana.set_index("Dia da Semana"))

        if st.button("Visualizar Query", key="btn_query_dia_semana"):
            st.session_state.show_query_dia_semana = not st.session_state.show_query_dia_semana
        
        if st.session_state.show_query_dia_semana:
            st.markdown("```sql\n" + query_dia_semana + "\n```")
    else:
        st.info("Nenhuma exibição encontrada para gerar o dashboard de dias da semana.")
else:
    st.error(resultado_dia_semana)

st.markdown("---")
st.header("🎟️ Análise de Filmes")
st.markdown("---")

st.subheader("Média de Duração dos Filmes por Ano")
ok_media_duracao, resultado_media_duracao, query_media_duracao = crud_filme.obter_media_duracao_filmes_por_ano()

if ok_media_duracao:
    if resultado_media_duracao:
        df_media_duracao = pd.DataFrame(resultado_media_duracao)
        df_media_duracao = df_media_duracao.rename(columns={'media_duracao': 'Média de Duração (min)'})
        
        fig_media_duracao = px.line(df_media_duracao, x="ano", y="Média de Duração (min)",
                                    labels={"ano": "Ano de Lançamento", "Média de Duração (min)": "Média de Duração (min)"}, markers=True)
        st.plotly_chart(fig_media_duracao, use_container_width=True)

        st.table(df_media_duracao.set_index("ano"))

        if st.button("Visualizar Query", key="btn_query_media_duracao"):
            st.session_state.show_query_media_duracao = not st.session_state.show_query_media_duracao
        
        if st.session_state.show_query_media_duracao:
            st.markdown("```sql\n" + query_media_duracao + "\n```")
    else:
        st.info("Nenhum dado de duração de filme encontrado para gerar o dashboard de média de duração.")
else:
    st.error(resultado_media_duracao)

st.markdown("---")

st.subheader("Filmes sem Exibições Agendadas")
ok_filmes_sem_exibicao, resultado_filmes_sem_exibicao, query_filmes_sem_exibicao = crud_filme.obter_filmes_sem_exibicao()

if ok_filmes_sem_exibicao:
    if resultado_filmes_sem_exibicao:
        df_filmes_sem_exibicao = pd.DataFrame(resultado_filmes_sem_exibicao)
        df_filmes_sem_exibicao = df_filmes_sem_exibicao.rename(columns={
            'filme_sem_exibicao': 'Filme',
            'ano': 'Ano',
            'duracao': 'Duração (min)'
        })
        st.table(df_filmes_sem_exibicao.set_index("Filme"))
        
        if st.button("Visualizar Query", key="btn_query_filmes_sem_exibicao"):
            st.session_state.show_query_filmes_sem_exibicao = not st.session_state.show_query_filmes_sem_exibicao
        
        if st.session_state.show_query_filmes_sem_exibicao:
            st.markdown("```sql\n" + query_filmes_sem_exibicao + "\n```")
    else:
        st.info("Todos os filmes possuem exibições agendadas ou nenhum filme cadastrado.")
else:
    st.error(resultado_filmes_sem_exibicao)

st.markdown("---")

st.subheader("Filmes sem Elenco Cadastrado")
ok_filmes_sem_elenco, resultado_filmes_sem_elenco, query_filmes_sem_elenco = crud_filme.obter_filmes_sem_elenco()

if ok_filmes_sem_elenco:
    if resultado_filmes_sem_elenco:
        df_filmes_sem_elenco = pd.DataFrame(resultado_filmes_sem_elenco)
        df_filmes_sem_elenco = df_filmes_sem_elenco.rename(columns={
            'filme_sem_elenco': 'Filme',
            'ano': 'Ano',
            'duracao': 'Duração (min)'
        })
        st.table(df_filmes_sem_elenco.set_index("Filme"))
        
        if st.button("Visualizar Query", key="btn_query_filmes_sem_elenco"):
            st.session_state.show_query_filmes_sem_elenco = not st.session_state.show_query_filmes_sem_elenco
        
        if st.session_state.show_query_filmes_sem_elenco:
            st.markdown("```sql\n" + query_filmes_sem_elenco + "\n```")
    else:
        st.info("Todos os filmes possuem elenco cadastrado ou nenhum filme encontrado.")
else:
    st.error(resultado_filmes_sem_elenco)

st.markdown("---")

st.subheader("Filmes com Exibições Futuras")
ok_filmes_futuros, resultado_filmes_futuros, query_filmes_futuros = crud_exibicao.obter_filmes_com_exibicoes_futuras()

if ok_filmes_futuros:
    if resultado_filmes_futuros:
        df_filmes_futuros = pd.DataFrame(resultado_filmes_futuros)
        for row in resultado_filmes_futuros:
            if isinstance(row['hora_exibicao'], timedelta):
                total_seconds = int(row['hora_exibicao'].total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                row['hora_exibicao'] = f"{hours:02d}:{minutes:02d}"
            elif isinstance(row['hora_exibicao'], time):
                row['hora_exibicao'] = row['hora_exibicao'].strftime('%H:%M')

        df_filmes_futuros = df_filmes_futuros.rename(columns={
            'filme': 'Filme',
            'canal': 'Canal',
            'data_exibicao': 'Data',
            'hora_exibicao': 'Hora'
        })
        st.table(df_filmes_futuros.set_index("Filme"))
        
        if st.button("Visualizar Query", key="btn_query_filmes_futuros"):
            st.session_state.show_query_filmes_futuros = not st.session_state.show_query_filmes_futuros
        
        if st.session_state.show_query_filmes_futuros:
            st.markdown("```sql\n" + query_filmes_futuros + "\n```")
    else:
        st.info("Nenhuma exibição futura encontrada.")
else:
    st.error(resultado_filmes_futuros)


st.markdown("---")
st.header("⭐ Análise de Elenco")
st.markdown("---")

st.subheader("Atores em Múltiplos Filmes")
ok_multi_ator, resultado_multi_ator, query_multi_ator = crud_elenco.obter_atores_em_multiplos_filmes()

if ok_multi_ator:
    if resultado_multi_ator:
        df_multi_ator = pd.DataFrame(resultado_multi_ator)
        df_multi_ator = df_multi_ator.rename(columns={
            'nome_ator': 'Ator/Atriz',
            'filmes_participados': 'Filmes Participados',
            'total_filmes': 'Total de Filmes'
        })
        
        st.table(df_multi_ator.set_index("Ator/Atriz"))
        
        if st.button("Visualizar Query", key="btn_query_multi_ator"):
            st.session_state.show_query_multi_ator = not st.session_state.show_query_multi_ator

        if st.session_state.show_query_multi_ator:
            st.markdown("```sql\n" + query_multi_ator + "\n```")
    else:
        st.info("Nenhum ator encontrado em múltiplos filmes nos dados atuais.")
else:
    st.error(resultado_multi_ator)

st.markdown("---")

st.subheader("Protagonistas em Múltiplos Filmes")
ok_proto_multi_ator, resultado_proto_multi_ator, query_proto_multi_ator = crud_elenco.obter_protagonistas_em_multiplos_filmes()

if ok_proto_multi_ator:
    if resultado_proto_multi_ator:
        df_proto_multi_ator = pd.DataFrame(resultado_proto_multi_ator)
        df_proto_multi_ator = df_proto_multi_ator.rename(columns={
            'nome_ator': 'Protagonista',
            'filmes_protagonizados': 'Filmes Protagonizados',
            'total_filmes_protagonista': 'Total de Filmes Protagonizados'
        })
        
        st.table(df_proto_multi_ator.set_index("Protagonista"))
        
        if st.button("Visualizar Query", key="btn_query_proto_multi_ator"):
            st.session_state.show_query_proto_multi_ator = not st.session_state.show_query_proto_multi_ator

        if st.session_state.show_query_proto_multi_ator:
            st.markdown("```sql\n" + query_proto_multi_ator + "\n```")
    else:
        st.info("Nenhum ator encontrado como protagonista em múltiplos filmes nos dados atuais.")
else:
    st.error(resultado_proto_multi_ator)

st.markdown("---")

st.subheader("Atores sem Papéis de Protagonista")
ok_ator_sem_proto, resultado_ator_sem_proto, query_ator_sem_proto = crud_elenco.obter_atores_sem_papeis_protagonista()

if ok_ator_sem_proto:
    if resultado_ator_sem_proto:
        df_ator_sem_proto = pd.DataFrame(resultado_ator_sem_proto)
        df_ator_sem_proto = df_ator_sem_proto.rename(columns={
            'nome_ator': 'Ator/Atriz',
            'filmes_atuados': 'Filmes Atuados (não protagonista)'
        })
        
        st.table(df_ator_sem_proto.set_index("Ator/Atriz"))
        
        if st.button("Visualizar Query", key="btn_query_ator_sem_proto"):
            st.session_state.show_query_ator_sem_proto = not st.session_state.show_query_ator_sem_proto
        
        if st.session_state.show_query_ator_sem_proto:
            st.markdown("```sql\n" + query_ator_sem_proto + "\n```")
    else:
        st.info("Todos os atores são protagonistas em pelo menos um filme ou nenhum ator encontrado sem protagonismo.")
else:
    st.error(resultado_ator_sem_proto)


st.markdown("---")
st.header("🍿 Análise de Canais")
st.markdown("---")

st.subheader("Variedade de Filmes por Canal")
ok_canais_variedade, resultado_canais_variedade, query_canais_variedade = crud_exibicao.obter_canais_por_variedade_filmes()

if ok_canais_variedade:
    if resultado_canais_variedade:
        df_canais_variedade = pd.DataFrame(resultado_canais_variedade)
        df_canais_variedade = df_canais_variedade.rename(columns={
            'nome_canal': 'Canal',
            'quantidade_filmes_unicos': 'Total de Filmes Únicos'
        })
        
        fig_canais_variedade = px.bar(df_canais_variedade, x="Canal", y="Total de Filmes Únicos",
                                      labels={"Total de Filmes Únicos": "Quantidade de Filmes Únicos"})
        st.plotly_chart(fig_canais_variedade, use_container_width=True)

        st.table(df_canais_variedade.set_index("Canal"))
        
        if st.button("Visualizar Query", key="btn_query_canais_variedade"):
            st.session_state.show_query_canais_variedade = not st.session_state.show_query_canais_variedade
        
        if st.session_state.show_query_canais_variedade:
            st.markdown("```sql\n" + query_canais_variedade + "\n```")
    else:
        st.info("Nenhum dado de canal ou exibição encontrado para esta análise.")
else:
    st.error(resultado_canais_variedade)

st.markdown("---")

st.subheader("Canais Ociosos (Próximos 30 Dias)")
ok_canais_ociosos, resultado_canais_ociosos, query_canais_ociosos = crud_exibicao.obter_canais_sem_exibicoes_proximos_30_dias()

if ok_canais_ociosos:
    if resultado_canais_ociosos:
        df_canais_ociosos = pd.DataFrame(resultado_canais_ociosos)
        df_canais_ociosos = df_canais_ociosos.rename(columns={
            'canal_ocioso': 'Canal'
        })
        
        st.table(df_canais_ociosos.set_index("Canal"))
        
        if st.button("Visualizar Query", key="btn_query_canais_ociosos"):
            st.session_state.show_query_canais_ociosos = not st.session_state.show_query_canais_ociosos
        
        if st.session_state.show_query_canais_ociosos:
            st.markdown("```sql\n" + query_canais_ociosos + "\n```")
    else:
        st.info("Todos os canais possuem exibições agendadas nos próximos 30 dias ou nenhum canal cadastrado.")
else:
    st.error(resultado_canais_ociosos)