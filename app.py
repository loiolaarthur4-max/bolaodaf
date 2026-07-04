import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Bolão da Família - Copa 2026", layout="wide")

st.title("🏆 Bolão da Família - Copa do Mundo 2026")

# Inicialização dos dados (em um caso real, você pode carregar de um CSV ou banco)
if 'participantes' not in st.session_state:
    st.session_state.participantes = pd.DataFrame({
        "Nome": ["Davi", "Arthur", "Victor", "Kharla", "Renan", "Fabio", "Tio Israel", "Tia Socorro", "Constantino", "Juliane", "Tino"],
        "Grupo": ["G1", "G1", "G1", "G1", "G2", "G2", "G2", "G2", "G3", "G3", "G3"],
        "Pontos": [0, 0, 55, 0, 30, 0, 0, 0, 10, 0, 0]
    })

def calcular_pontos(atual, acerto_placar, acerto_vencedor, erro):
    pontos = atual + (acerto_placar * 5) + (acerto_vencedor * 3)
    if erro:
        if pontos >= 50:
            pontos -= 3
    return max(0, pontos) # Garante que nunca fique negativo

# Interface do App
st.sidebar.header("Registrar Pontuação")
nome = st.sidebar.selectbox("Participante", st.session_state.participantes["Nome"])
acerto_placar = st.sidebar.number_input("Acertos de Placar", min_value=0)
acerto_venc = st.sidebar.number_input("Acertos de Vencedor", min_value=0)
erros = st.sidebar.number_input("Erros", min_value=0)

if st.sidebar.button("Atualizar Pontuação"):
    idx = st.session_state.participantes[st.session_state.participantes["Nome"] == nome].index[0]
    atual = st.session_state.participantes.at[idx, "Pontos"]
    novo_total = calcular_pontos(atual, acerto_placar, acerto_venc, erros > 0)
    st.session_state.participantes.at[idx, "Pontos"] = novo_total
    st.rerun()

# Exibição do Ranking
st.subheader("📊 Ranking do Bolão")
df_ranking = st.session_state.participantes.sort_values(by="Pontos", ascending=False)
st.table(df_ranking)

st.info("Regra: Se atingir 50 pontos ou mais, erros descontam 3 pontos. A pontuação nunca fica negativa.")
