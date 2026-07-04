import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Bolão da Família 2026", layout="wide")

# --- CARREGAR DADOS ---
if os.path.exists("bolao.csv"):
    st.session_state.palpites = pd.read_csv("bolao.csv")
else:
    st.session_state.palpites = pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])

if 'jogos' not in st.session_state: st.session_state.jogos = []

# --- LÓGICA DE LOGIN ---
if 'user_info' not in st.session_state: st.session_state.user_info = None

st.sidebar.header("🔐 Login")
tipo = st.sidebar.radio("Tipo de Acesso:", ["Membro", "Administrador"])

if tipo == "Administrador":
    senha = st.sidebar.text_input("Senha Admin", type="password")
    if senha == "davi2203":
        st.session_state.user_info = {"Nome": "Davi", "Grupo": "Grupo 1", "Admin": True}
        st.sidebar.success("Logado como Davi (Admin)")
else:
    grupo = st.sidebar.selectbox("Grupo:", ["Grupo 1", "Grupo 2", "Grupo 3"])
    senha = st.sidebar.text_input("Senha", type="password")
    senhas = {"Grupo 1": "vitones", "Grupo 2": "raelzinho", "Grupo 3": "tininho"}
    if senha == senhas.get(grupo):
        nomes = {"Grupo 1": ["Davi", "Arthur", "Victor", "Kharla"], 
                 "Grupo 2": ["Renan", "Fabio", "Tio Israel", "Tia Socorro"],
                 "Grupo 3": ["Constantino", "Juliane", "Tino"]}
        nome = st.sidebar.selectbox("Quem é você?", nomes[grupo])
        if st.sidebar.button("Entrar"):
            st.session_state.user_info = {"Nome": nome, "Grupo": grupo, "Admin": False}

# --- ABAS PRINCIPAIS ---
tab1, tab2, tab3 = st.tabs(["📊 Classificação", "📝 Palpites", "🛠️ Admin"])

with tab1:
    st.subheader("📊 Classificação Geral")
    if not st.session_state.palpites.empty:
        tabela = st.session_state.palpites.groupby(["Nome", "Grupo"])["Pontos"].sum().sort_values(ascending=False).reset_index()
        tabela.insert(0, "Posição", range(1, len(tabela) + 1))
        st.table(tabela)

with tab2:
    st.subheader("📝 Registrar Palpite")
    if st.session_state.user_info:
        jogo = st.selectbox("Jogo:", st.session_state.jogos)
        palpite = st.text_input("Seu palpite:")
        if st.button("Enviar Palpite"):
            nova = pd.DataFrame([[st.session_state.user_info["Nome"], st.session_state.user_info["Grupo"], jogo, palpite, 0]], 
                                columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
            st.session_state.palpites = pd.concat([st.session_state.palpites, nova], ignore_index=True)
            st.session_state.palpites.to_csv("bolao.csv", index=False)
            st.success("Palpite enviado!")
    else:
        st.warning("Faça login na barra lateral para palpitar.")

with tab3:
    st.subheader("🛠️ Ferramentas do Davi")
    if st.session_state.user_info and st.session_state.user_info["Admin"]:
        # Adicionar/Remover Jogos
        novo_jogo = st.text_input("Novo Jogo:")
        if st.button("Adicionar Jogo"): st.session_state.jogos.append(novo_jogo)
        
        jogo_del = st.selectbox("Remover Jogo:", st.session_state.jogos)
        if st.button("Deletar Jogo"): st.session_state.jogos.remove(jogo_del)
        
        # Ajustar Ranking
        nome_ajuste = st.selectbox("Ajustar pontos de:", st.session_state.palpites["Nome"].unique() if not st.session_state.palpites.empty else [])
        novo_pts = st.number_input("Novos Pontos:", value=0)
        if st.button("Salvar Pontos"):
            st.session_state.palpites.loc[st.session_state.palpites["Nome"] == nome_ajuste, "Pontos"] = novo_pts
            st.session_state.palpites.to_csv("bolao.csv", index=False)
            st.rerun()
    else:
        st.error("Área restrita apenas para o Administrador.")
