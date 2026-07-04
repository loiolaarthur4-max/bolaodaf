import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Bolão da Família 2026", layout="wide")

# --- BANCO DE DADOS (CARREGAMENTO) ---
if os.path.exists("bolao.csv"):
    st.session_state.palpites = pd.read_csv("bolao.csv")
else:
    st.session_state.palpites = pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])

if 'jogos' not in st.session_state: st.session_state.jogos = {}

# --- FUNÇÃO PARA SALVAR ---
def salvar():
    st.session_state.palpites.to_csv("bolao.csv", index=False)

# --- LOGIN ---
st.sidebar.header("🔐 Login")
tipo_login = st.sidebar.radio("Como deseja acessar?", ["Membro de Grupo", "Administrador"])

# --- ADMIN ---
if tipo_login == "Administrador":
    senha_adm = st.sidebar.text_input("Senha do Administrador", type="password")
    if senha_adm == "davi2203":
        st.sidebar.success("Acesso Admin Liberado")
        st.subheader("🛠️ Painel do Administrador (Davi)")
        
        novo_jogo = st.text_input("Adicionar Jogo")
        if st.button("Criar Jogo"):
            st.session_state.jogos[novo_jogo] = "Aberto"
        
        # Gestão de Jogos e Ajuste de Ranking
        st.write("Jogos Ativos:", st.session_state.jogos)
        
        nome_ajuste = st.selectbox("Ajustar Pontos de:", ["Davi", "Arthur", "Victor", "Kharla", "Renan", "Fabio", "Tio Israel", "Tia Socorro", "Constantino", "Juliane", "Tino"])
        pts_ajuste = st.number_input("Novo total de pontos:", value=0)
        if st.button("Atualizar Pontuação"):
            st.session_state.palpites.loc[st.session_state.palpites["Nome"] == nome_ajuste, "Pontos"] = pts_ajuste
            salvar()
            st.rerun()
    else:
        st.warning("Insira a senha do Admin na barra lateral.")

# --- MEMBRO DE GRUPO ---
else:
    grupo_sel = st.selectbox("Seu Grupo:", ["Grupo 1", "Grupo 2", "Grupo 3"])
    senha_gp = st.text_input("Senha do Grupo", type="password")
    senhas = {"Grupo 1": "vitones", "Grupo 2": "raelzinho", "Grupo 3": "tininho"}
    
    if senha_gp == senhas.get(grupo_sel):
        st.success(f"Logado como {grupo_sel}")
        participantes = {"Grupo 1": ["Davi", "Arthur", "Victor", "Kharla"], 
                         "Grupo 2": ["Renan", "Fabio", "Tio Israel", "Tia Socorro"],
                         "Grupo 3": ["Constantino", "Juliane", "Tino"]}
        
        nome = st.selectbox("Seu nome:", participantes[grupo_sel])
        jogo = st.selectbox("Jogo:", list(st.session_state.jogos.keys()))
        palpite = st.text_input("Seu palpite:")
        
        if st.button("Enviar Palpite"):
            nova = pd.DataFrame([[nome, grupo_sel, jogo, palpite, 0]], columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
            st.session_state.palpites = pd.concat([st.session_state.palpites, nova], ignore_index=True)
            salvar()
            st.success("Palpite enviado!")

# --- CLASSIFICAÇÃO ---
st.subheader("📊 Classificação Geral")
if not st.session_state.palpites.empty:
    ranking = st.session_state.palpites.groupby(["Nome", "Grupo"])["Pontos"].sum().sort_values(ascending=False).reset_index()
    st.table(ranking)
else:
    st.info("Nenhum palpite registrado ainda.")
