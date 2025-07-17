import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import crud_exibicao

st.title("📊 Dashboard de Exibições")
st.markdown("Esta seção apresenta um **gráfico** com insights sobre a programação de filmes. Abaixo, temos a quantidade de exibições por canal de TV, com base nos dados atuais.")

ok, resultado = crud_exibicao.obter_contagem_exibicoes_por_canal()
if ok:
 
    df = pd.DataFrame(resultado, columns=["Canal", "Total de Exibições"]).set_index("Canal")
    st.bar_chart(df)
    st.table(df)
else:
    st.error(resultado)
