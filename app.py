import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Bolão da Família 2026", layout="wide")

# --- CARREGAR DADOS ---
if os.path.exists("bolao.csv"):
    st.session_state.palpites = pd.read_csv("bolao.csv")
else:
    st.session_state.palpites = pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])

# --- MENU DE LOGIN ---
st.sidebar.header("🔐 Acesso")
tipo_login = st.sidebar.radio("Tipo:", ["Membro de Grupo", "Administrador"])

# --- ESTRUTURA COM ABAS (ORGANIZAÇÃO) ---
tab_ranking, tab_palpites, tab_admin = st.tabs(["📊 Classificação", "📝 Palpites", "🛠️ Admin (Davi)"])

# 1. ABA DE CLASSIFICAÇÃO (PARA TODOS)
with tab_ranking:
    st.subheader("📊 Classificação Geral")
    if not st.session_state.palpites.empty:
        tabela = st.session_state.palpites.groupby(["Nome", "Grupo"])["Pontos"].sum().sort_values(ascending=False).reset_index()
        tabela.insert(0, "Posição", range(1, len(tabela) + 1))
        st.table(tabela)
    else:
        st.write("Nenhum palpite registrado ainda.")

# 2. ABA DE PALPITES (FAMÍLIA)
with tab_palpites:
    st.subheader("📝 Registrar Palpite")
    if tipo_login == "Membro de Grupo":
        grupo_sel = st.selectbox("Selecione seu Grupo:", ["Grupo 1", "Grupo 2", "Grupo 3"])
        senha_gp = st.text_input("Senha do Grupo", type="password")
        senhas = {"Grupo 1": "vitones", "Grupo 2": "raelzinho", "Grupo 3": "tininho"}
        
        if senha_gp == senhas.get(grupo_sel):
            participantes = {"Grupo 1": ["Davi", "Arthur", "Victor", "Kharla"], 
                             "Grupo 2": ["Renan", "Fabio", "Tio Israel", "Tia Socorro"],
                             "Grupo 3": ["Constantino", "Juliane", "Tino"]}
            nome = st.selectbox("Seu nome:", participantes[grupo_sel])
            jogo = st.text_input("Jogo:")
            palpite = st.text_input("Seu palpite:")
            if st.button("Enviar"):
                nova = pd.DataFrame([[nome, grupo_sel, jogo, palpite, 0]], columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
                st.session_state.palpites = pd.concat([st.session_state.palpites, nova], ignore_index=True)
                st.session_state.palpites.to_csv("bolao.csv", index=False)
                st.success("Palpite salvo!")
        else:
            st.warning("Senha incorreta ou grupo não selecionado.")
    else:
        st.info("Logue como Membro de Grupo para registrar palpites.")

# 3. ABA DO ADMIN (DAVI)
with tab_admin:
    st.subheader("🛠️ Área Restrita (Davi)")
    senha_adm = st.text_input("Senha Admin", type="password")
    if senha_adm == "davi2203":
        nome_ajuste = st.selectbox("Ajustar Pontos de quem?", st.session_state.palpites["Nome"].unique() if not st.session_state.palpites.empty else [])
        novo_pts = st.number_input("Novos Pontos:", value=0)
        if st.button("Salvar Pontos"):
            st.session_state.palpites.loc[st.session_state.palpites["Nome"] == nome_ajuste, "Pontos"] = novo_pts
            st.session_state.palpites.to_csv("bolao.csv", index=False)
            st.rerun()
    else:
        st.error("Senha de administrador necessária.")
