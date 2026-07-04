import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(page_title="Bolão Davi Admin", layout="wide")

# --- ARQUIVOS DE DADOS ---
PALPITES_FILE = "palpites.csv"
JOGOS_FILE = "jogos.csv"
PARTICIPANTES_FILE = "participantes.csv"

def carregar(file, cols):
    if os.path.exists(file): return pd.read_csv(file)
    return pd.DataFrame(columns=cols)

# Carrega os dados para o estado da sessão
if 'palpites' not in st.session_state: st.session_state.palpites = carregar(PALPITES_FILE, ["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
if 'jogos' not in st.session_state: st.session_state.jogos = carregar(JOGOS_FILE, ["Nome_Jogo", "Status"])
if 'part' not in st.session_state: st.session_state.part = carregar(PARTICIPANTES_FILE, ["Nome", "Grupo"])

# --- LOGIN PERSISTENTE ---
st.sidebar.header("🔐 Acesso")
query_params = st.query_params
senha = query_params.get("senha", st.sidebar.text_input("Senha:", type="password"))

if st.sidebar.button("Entrar"):
    st.query_params["senha"] = senha
    st.rerun()

modo_admin = (senha == "davi2203")
modo_membro = (senha in ["vitones", "raelzinho", "tininho"])

if st.sidebar.button("Sair"):
    st.query_params.clear()
    st.rerun()

# --- INTERFACE ---
tab1, tab2 = st.tabs(["📊 Bolão", "🛠️ Painel do Davi"])

with tab1:
    st.subheader("Classificação Geral")
    if not st.session_state.palpites.empty:
        st.table(st.session_state.palpites.groupby(["Nome", "Grupo"])["Pontos"].sum().sort_values(ascending=False))
    
    st.markdown("---")
    st.subheader("Registrar Palpite")
    if modo_membro or modo_admin:
        with st.form("palpite_form"):
            nome = st.text_input("Seu Nome:")
            jogo = st.selectbox("Jogo:", st.session_state.jogos["Nome_Jogo"].tolist() if not st.session_state.jogos.empty else [])
            palpite = st.text_input("Placar (ex: 2x1):")
            if st.form_submit_button("Enviar"):
                nova = pd.DataFrame([[nome, "N/A", jogo, palpite, 0]], columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
                st.session_state.palpites = pd.concat([st.session_state.palpites, nova], ignore_index=True)
                st.session_state.palpites.to_csv(PALPITES_FILE, index=False)
                st.success("Palpite enviado!")
                st.rerun()
    else:
        st.warning("Insira a senha fornecida pelo Davi para acessar.")

with tab2:
    if modo_admin:
        st.subheader("⚠️ Painel de Controle Total (Davi)")
        st.write("Edite as tabelas abaixo e salve para aplicar as mudanças.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write("### 🎮 Jogos")
            st.session_state.jogos = st.data_editor(st.session_state.jogos, num_rows="dynamic")
        with c2:
            st.write("### 👥 Participantes")
            st.session_state.part = st.data_editor(st.session_state.part, num_rows="dynamic")
        with c3:
            st.write("### 📝 Palpites")
            st.session_state.palpites = st.data_editor(st.session_state.palpites, num_rows="dynamic")
            
        if st.button("💾 SALVAR TUDO"):
            st.session_state.jogos.to_csv(JOGOS_FILE, index=False)
            st.session_state.part.to_csv(PARTICIPANTES_FILE, index=False)
            st.session_state.palpites.to_csv(PALPITES_FILE, index=False)
            st.success("Alterações salvas com sucesso!")
            st.rerun()
    else:
        st.error("Acesso restrito: Apenas o Administrador pode editar a base de dados.")
