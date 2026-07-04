import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Bolão da Família 2026", layout="wide")

# --- CARREGAR DADOS ---
if os.path.exists("bolao.csv"):
    st.session_state.palpites = pd.read_csv("bolao.csv")
else:
    st.session_state.palpites = pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])

# --- LOGIN E ADMIN ---
st.sidebar.header("🔐 Acesso")
tipo_login = st.sidebar.radio("Tipo:", ["Membro", "Administrador"])

if tipo_login == "Administrador":
    senha = st.sidebar.text_input("Senha Admin", type="password")
    if senha == "davi2203":
        st.subheader("🛠️ Painel do Administrador (Davi)")
        novo_jogo = st.text_input("Novo Jogo")
        if st.button("Criar Jogo"): 
            if 'jogos' not in st.session_state: st.session_state.jogos = []
            st.session_state.jogos.append(novo_jogo)
        
        # Ajuste de Pontos
        nome_ajuste = st.selectbox("Ajustar Pontos de:", st.session_state.palpites["Nome"].unique() if not st.session_state.palpites.empty else [])
        novo_pts = st.number_input("Pontos:", value=0)
        if st.button("Salvar Pontos"):
            st.session_state.palpites.loc[st.session_state.palpites["Nome"] == nome_ajuste, "Pontos"] = novo_pts
            st.session_state.palpites.to_csv("bolao.csv", index=False)
            st.rerun()

# --- CLASSIFICAÇÃO (A TABELA QUE VOCÊ QUER VER) ---
st.subheader("📊 Classificação Geral")

if not st.session_state.palpites.empty:
    # Agrupa para mostrar o total de cada um
    tabela = st.session_state.palpites.groupby(["Nome", "Grupo"])["Pontos"].sum().sort_values(ascending=False).reset_index()
    # Adiciona a numeração de posição (1º, 2º, 3º...)
    tabela.insert(0, "Posição", range(1, len(tabela) + 1))
    st.table(tabela)
else:
    # Tabela vazia com cabeçalhos para não ficar feio
    st.write("Nenhum palpite registrado. A tabela aparecerá aqui assim que o primeiro palpite for enviado!")
    st.table(pd.DataFrame(columns=["Posição", "Nome", "Grupo", "Pontos"]))
