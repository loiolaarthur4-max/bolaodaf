import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Bolão da Família", layout="wide")
DB_FILE = "bolao_total.csv"

# --- BANCO DE DADOS ---
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"]).to_csv(DB_FILE, index=False)

st.session_state.df = pd.read_csv(DB_FILE)

# --- LOGIN E AJUDA ---
st.sidebar.header("🔐 Login")

# Guia de Acesso (para o pessoal saber de qual grupo é)
with st.sidebar.expander("ℹ️ Preciso de ajuda para logar"):
    st.write("• **Grupo 1:** Davi, Arthur, Victor, Kharla (Senha: vitones)")
    st.write("• **Grupo 2:** Renan, Fabio, Tio Israel, Tia Socorro (Senha: raelzinho)")
    st.write("• **Grupo 3:** Constantino, Juliane, Tino (Senha: tininho)")

# Input de Login
senha_digitada = st.sidebar.text_input("Digite sua senha:", type="password")

# --- LÓGICA DE NÍVEIS DE ACESSO ---
if senha_digitada == "davi2203":
    st.sidebar.success("Modo Admin: Controle Total")
    acesso = "admin"
elif senha_digitada in ["vitones", "raelzinho", "tininho"]:
    acesso = "membro"
    st.sidebar.info("Modo Membro: Registrando Palpites")
else:
    acesso = None
    if senha_digitada: st.sidebar.error("Senha inválida.")

# --- INTERFACE ---
tab1, tab2 = st.tabs(["📊 Classificação e Palpites", "🛠️ Painel do Davi (Edição Total)"])

with tab1:
    st.subheader("Classificação Geral")
    st.table(st.session_state.df.groupby(["Nome", "Grupo"])["Pontos"].sum().sort_values(ascending=False))
    
    st.markdown("---")
    st.subheader("Registrar Novo Palpite")
    if acesso in ["membro", "admin"]:
        with st.form("palpite_form"):
            nome = st.text_input("Seu Nome:")
            grupo = st.selectbox("Seu Grupo:", ["Grupo 1", "Grupo 2", "Grupo 3"])
            jogo = st.text_input("Nome do Jogo:")
            palpite = st.text_input("Seu Palpite:")
            if st.form_submit_button("Enviar"):
                nova = pd.DataFrame([[nome, grupo, jogo, palpite, 0]], columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
                pd.concat([st.session_state.df, nova], ignore_index=True).to_csv(DB_FILE, index=False)
                st.rerun()
    else:
        st.warning("Faça login na barra lateral para palpitar.")

with tab2:
    if acesso == "admin":
        st.subheader("⚠️ Área de Edição Master")
        st.write("Davi, você pode editar a tabela abaixo diretamente. Clique nas células para mudar pontos, apagar palpites ou corrigir nomes.")
        
        # O Editor Total
        novo_df = st.data_editor(st.session_state.df, num_rows="dynamic")
        if st.button("Salvar Todas as Alterações"):
            novo_df.to_csv(DB_FILE, index=False)
            st.success("Dados salvos com sucesso!")
            st.rerun()
    else:
        st.error("Acesso restrito: Esta área é exclusiva para o Davi.")
