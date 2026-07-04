import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Bolão da Família", layout="wide")
DB_FILE = "bolao_total.csv"

# --- BANCO DE DADOS ---
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"]).to_csv(DB_FILE, index=False)
st.session_state.df = pd.read_csv(DB_FILE)

# --- LOGIN SIMPLIFICADO ---
st.sidebar.header("🔐 Acesso")
senha = st.sidebar.text_input("Digite a senha que o Davi te enviou:", type="password")

# Define quem é Admin e quem é Membro
modo_admin = (senha == "davi2203")
modo_membro = (senha in ["vitones", "raelzinho", "tininho"])

# --- INTERFACE ---
tab1, tab2 = st.tabs(["📊 Classificação e Palpites", "🛠️ Painel do Davi (Admin)"])

with tab1:
    st.subheader("Classificação Geral")
    st.table(st.session_state.df.groupby(["Nome", "Grupo"])["Pontos"].sum().sort_values(ascending=False))
    
    st.markdown("---")
    st.subheader("Registrar seu Palpite")
    if modo_membro or modo_admin:
        with st.form("palpite_form"):
            nome = st.text_input("Seu Nome:")
            grupo = st.selectbox("Seu Grupo:", ["Grupo 1", "Grupo 2", "Grupo 3"])
            jogo = st.text_input("Nome do Jogo:")
            palpite = st.text_input("Seu Palpite:")
            if st.form_submit_button("Enviar Palpite"):
                nova = pd.DataFrame([[nome, grupo, jogo, palpite, 0]], columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
                pd.concat([st.session_state.df, nova], ignore_index=True).to_csv(DB_FILE, index=False)
                st.success("Palpite registrado!")
                st.rerun()
    else:
        st.warning("Insira a senha que você recebeu no WhatsApp para acessar.")

with tab2:
    if modo_admin:
        st.subheader("⚠️ Painel de Controle Total")
        st.write("Davi, aqui você controla tudo. Edite a tabela abaixo como se fosse um Excel.")
        
        # Edição total
        novo_df = st.data_editor(st.session_state.df, num_rows="dynamic")
        
        if st.button("SALVAR TODAS AS ALTERAÇÕES"):
            novo_df.to_csv(DB_FILE, index=False)
            st.success("Dados atualizados com sucesso!")
            st.rerun()
    else:
        st.error("Acesso restrito ao Administrador.")
