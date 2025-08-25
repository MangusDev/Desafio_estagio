import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import uuid
from utils.apis import (
    buscar_artigos_pubmed,
    buscar_patentes,
    buscar_google_scholar,
    carregar_dados_publicos
)
from utils.db import salvar_interacao, listar_interacoes

# ----------------------------
# Funções mock simulando APIs
# ----------------------------

def buscar_artigos_pubmed(tema):
    return pd.DataFrame({
        "Título": [f"Estudo clínico sobre {tema}", f"Nova abordagem para {tema}"],
        "Autores": ["Silva et al.", "Souza et al."],
        "Ano": [2022, 2023],
        "Fonte": ["PubMed", "PubMed"]
    })

def buscar_patentes(tema):
    return pd.DataFrame({
        "Título da Patente": [f"Dispositivo para {tema}", f"Método de {tema}"],
        "Número": ["US123456", "US789012"],
        "Ano": [2021, 2020],
        "Fonte": ["PatentsView", "PatentsView"]
    })

# ----------------------------
# Configuração do Streamlit
# ----------------------------

st.set_page_config(page_title="Jornada SaúdeJá", layout="wide")
st.title("🧬 Jornada Interativa de Inovação em Saúde")

# ----------------------------
# Identificador anônimo do usuário
# ----------------------------

if "usuario_id" not in st.session_state:
    st.session_state["usuario_id"] = str(uuid.uuid4())

# ----------------------------
# Entrada do usuário
# ----------------------------

tema = st.text_input("Digite o tema de pesquisa médica (ex.: tratamento de diabetes)")

if st.button("Explorar Oportunidades") and tema:
    salvar_interacao(tema, st.session_state["usuario_id"])

    st.subheader("📚 Artigos Científicos")
    artigos = buscar_artigos_pubmed(tema)
    st.dataframe(artigos)

    st.subheader("🔬 Patentes Relacionadas")
    patentes = buscar_patentes(tema)
    st.dataframe(patentes)

    st.subheader("📊 Visualização de Publicações por Ano")
    fig, ax = plt.subplots()
    artigos["Ano"].value_counts().sort_index().plot(kind="bar", ax=ax, color="skyblue")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Número de Artigos")
    ax.set_title("Distribuição de Artigos Científicos")
    st.pyplot(fig)

    st.success("Interação registrada com sucesso!")

# ----------------------------
# Histórico de interações
# ----------------------------

with st.expander("📁 Ver últimas interações salvas"):
    interacoes = listar_interacoes()
    if interacoes:
        df = pd.DataFrame(interacoes)
        st.dataframe(df)
    else:
        st.info("Nenhuma interação registrada ainda.")

# ----------------------------
# Rodapé
# ----------------------------

st.markdown("---")
st.caption("🔒 Dados anonimizados conforme LGPD. Desenvolvido para o desafio Mastera.")