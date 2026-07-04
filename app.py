import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Bolão Admin", layout="wide")

# --- ARQUIVOS DE DADOS ---
PALPITES_FILE = "palpites.csv"
JOGOS_FILE = "jogos.csv"
PARTICIPANTES_FILE = "participantes.csv"

def carregar(file, cols):
    if os.path.exists(file): return pd.read_csv(file)
    return pd.DataFrame(columns=cols)

# Carrega os dados
df_palpites = carregar(PALPITES_FILE, ["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
df_jogos = carregar(JOGOS_FILE, ["Nome_Jogo", "Status"])
df_part = carregar(PARTICIPANTES_FILE, ["Nome", "Grupo"])

# --- LOGIN SIMPLIFICADO ---
st.sidebar.header("🔐 Acesso")
senha = st.sidebar.text_input("Senha:", type="password")
modo_admin = (senha == "davi2203")
modo_membro = (senha in ["vitones", "raelzinho", "tininho"])

# --- ABAS ---
tab1, tab2 = st.tabs(["📊 Bolão", "🛠️ Painel do Davi"])

with tab1:
    st.subheader("Classificação")
    st.table(df_palpites.groupby(["Nome", "Grupo"])["Pontos"].sum().sort_values(ascending=False))
    
    st.markdown("---")
    if modo_membro or modo_admin:
        with st.form("palpite"):
            nome = st.text_input("Seu Nome:")
            jogo = st.selectbox("Jogo:", df_jogos["Nome_Jogo"].tolist() if not df_jogos.empty else [])
            palpite = st.text_input("Placar:")
            if st.form_submit_button("Enviar"):
                nova = pd.DataFrame([[nome, "Grupo X", jogo, palpite, 0]], columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
                pd.concat([df_palpites, nova], ignore_index=True).to_csv(PALPITES_FILE, index=False)
                st.rerun()
    else:
        st.warning("Insira a senha.")

with tab2:
    if modo_admin:
        st.subheader("⚠️ Controle Total do Davi")
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.write("### 🎮 Jogos")
            edit_jogos = st.data_editor(df_jogos, num_rows="dynamic")
        with c2:
            st.write("### 👥 Participantes")
            edit_part = st.data_editor(df_part, num_rows="dynamic")
        with c3:
            st.write("### 📝 Palpites")
            edit_palpites = st.data_editor(df_palpites, num_rows="dynamic")
            
        if st.button("💾 SALVAR TODAS AS ALTERAÇÕES"):
            edit_jogos.to_csv(JOGOS_FILE, index=False)
            edit_part.to_csv(PARTICIPANTES_FILE, index=False)
            edit_palpites.to_csv(PALPITES_FILE, index=False)
            st.success("Tudo salvo com sucesso!")
            st.rerun()
    else:
        st.error("Área restrita.")
