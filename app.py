import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(page_title="Bolão da Família 2026", layout="wide")

# --- CARREGAMENTO DE DADOS ---
if 'config' not in st.session_state: st.session_state.config = {"titulo": "⚽ Bolão da Família - Copa 2026"}
if 'jogos' not in st.session_state: st.session_state.jogos = []
if os.path.exists("bolao.csv"):
    st.session_state.palpites = pd.read_csv("bolao.csv")
else:
    st.session_state.palpites = pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])

# --- LOGIN ---
if 'user' not in st.session_state: st.session_state.user = None

with st.sidebar:
    st.header("🔐 Login")
    if not st.session_state.user:
        tipo = st.radio("Acesso:", ["Membro", "Administrador"])
        if tipo == "Administrador":
            senha = st.text_input("Senha Admin", type="password")
            if st.button("Entrar Admin"):
                if senha == "davi2203":
                    st.session_state.user = {"Nome": "Davi", "Grupo": "Grupo 1", "Admin": True}
                    st.rerun()
        else:
            grupo = st.selectbox("Grupo:", ["Grupo 1", "Grupo 2", "Grupo 3"])
            senha = st.text_input("Senha", type="password")
            senhas = {"Grupo 1": "vitones", "Grupo 2": "raelzinho", "Grupo 3": "tininho"}
            if st.button("Entrar"):
                if senha == senhas.get(grupo):
                    participantes = {"Grupo 1": ["Davi", "Arthur", "Victor", "Kharla"], 
                                     "Grupo 2": ["Renan", "Fabio", "Tio Israel", "Tia Socorro"],
                                     "Grupo 3": ["Constantino", "Juliane", "Tino"]}
                    nome = st.selectbox("Quem é você?", participantes[grupo])
                    if st.button("Confirmar Nome"):
                        st.session_state.user = {"Nome": nome, "Grupo": grupo, "Admin": False}
                        st.rerun()
    else:
        st.write(f"Logado: **{st.session_state.user['Nome']}**")
        if st.button("Sair"): st.session_state.user = None; st.rerun()

# --- TÍTULO DINÂMICO ---
st.title(st.session_state.config["titulo"])

# --- ABAS ---
tab1, tab2, tab3 = st.tabs(["📊 Classificação", "📝 Palpites", "🛠️ Painel do Davi"])

with tab1:
    st.subheader("Classificação Geral")
    if not st.session_state.palpites.empty:
        rank = st.session_state.palpites.groupby(["Nome", "Grupo"])["Pontos"].sum().sort_values(ascending=False).reset_index()
        rank.index = range(1, len(rank) + 1)
        st.table(rank)
    else: st.info("Nenhum palpite ainda.")

with tab2:
    if st.session_state.user:
        jogo = st.selectbox("Escolha o Jogo:", st.session_state.jogos)
        palpite = st.text_input("Seu palpite (ex: 2x1):")
        if st.button("Enviar Palpite"):
            nova = pd.DataFrame([[st.session_state.user["Nome"], st.session_state.user["Grupo"], jogo, palpite, 0]], 
                                columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
            st.session_state.palpites = pd.concat([st.session_state.palpites, nova], ignore_index=True)
            st.session_state.palpites.to_csv("bolao.csv", index=False)
            st.success("Registrado!")
    else: st.warning("Faça login na barra lateral.")

with tab3:
    if st.session_state.user and st.session_state.user["Admin"]:
        st.subheader("Controle Total")
        st.session_state.config["titulo"] = st.text_input("Alterar Título do Site:", value=st.session_state.config["titulo"])
        
        # Gestão de Jogos
        novo_j = st.text_input("Adicionar Jogo:")
        if st.button("Adicionar"): st.session_state.jogos.append(novo_j); st.rerun()
        
        del_j = st.selectbox("Remover Jogo:", st.session_state.jogos)
        if st.button("Remover"): st.session_state.jogos.remove(del_j); st.rerun()
        
        # Gestão de Pontos
        nome_adj = st.selectbox("Ajustar pontos de:", st.session_state.palpites["Nome"].unique() if not st.session_state.palpites.empty else [])
        pts_adj = st.number_input("Novo Total de Pontos:", value=0)
        if st.button("Salvar Pontos"):
            st.session_state.palpites.loc[st.session_state.palpites["Nome"] == nome_adj, "Pontos"] = pts_adj
            st.session_state.palpites.to_csv("bolao.csv", index=False); st.rerun()
            
        if st.button("⚠️ LIMPAR TUDO"):
            st.session_state.palpites = pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
            st.session_state.palpites.to_csv("bolao.csv", index=False); st.rerun()
    else: st.error("Acesso restrito.")
