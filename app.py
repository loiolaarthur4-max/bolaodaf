import streamlit as st
import pandas as pd
import os

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Bolão da Família", layout="wide")
DB_FILE = "bolao_total.csv"

def carregar():
    if os.path.exists(DB_FILE): return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])

if 'df' not in st.session_state: st.session_state.df = carregar()

# --- LOGIN ---
st.sidebar.header("🔐 Login")
senha = st.sidebar.text_input("Sua senha:", type="password")

# --- LÓGICA DE ACESSO ---
# Se for a sua senha, libera o modo "DEUS" (Davi)
if senha == "davi2203":
    st.sidebar.success("Modo Admin: Controle Total")
    modo_admin = True
# Se for senha de grupo, libera modo "MEMBRO"
elif senha in ["vitones", "raelzinho", "tininho"]:
    modo_admin = False
    st.sidebar.info("Modo Membro: Registrando Palpites")
else:
    modo_admin = False
    st.sidebar.warning("Senha incorreta ou não informada.")

# --- ABAS ---
tab1, tab2 = st.tabs(["📊 Classificação e Palpites", "🛠️ Painel do Davi (Controle Total)"])

with tab1:
    st.subheader("Classificação Atual")
    st.table(st.session_state.df.groupby(["Nome", "Grupo"])["Pontos"].sum().sort_values(ascending=False))
    
    st.subheader("Registrar Novo Palpite")
    with st.form("palpite_form"):
        nome = st.text_input("Seu Nome:")
        grupo = st.selectbox("Seu Grupo:", ["Grupo 1", "Grupo 2", "Grupo 3"])
        jogo = st.text_input("Nome do Jogo:")
        palpite = st.text_input("Seu Palpite:")
        if st.form_submit_button("Enviar"):
            nova_linha = pd.DataFrame([[nome, grupo, jogo, palpite, 0]], columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
            st.session_state.df = pd.concat([st.session_state.df, nova_linha], ignore_index=True)
            st.session_state.df.to_csv(DB_FILE, index=False)
            st.rerun()

with tab2:
    if modo_admin:
        st.subheader("⚠️ Painel de Edição Total")
        st.write("Davi, você pode editar qualquer coisa abaixo, apagar linhas ou mudar pontos. O que você salvar aqui, vale para todos.")
        
        # O Editor Total
        novo_df = st.data_editor(st.session_state.df, num_rows="dynamic")
        if st.button("Salvar Todas as Alterações"):
            st.session_state.df = novo_df
            st.session_state.df.to_csv(DB_FILE, index=False)
            st.rerun()
            
        if st.button("Resetar Todo o Banco de Dados"):
            st.session_state.df = pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
            st.session_state.df.to_csv(DB_FILE, index=False)
            st.rerun()
    else:
        st.error("Acesso restrito: Apenas o Davi pode editar a base de dados.")
