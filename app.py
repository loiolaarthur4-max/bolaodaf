import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bolão da Família 2026", layout="wide")

# --- BANCO DE DADOS ---
participantes_db = {
    "Davi": "Grupo 1", "Arthur": "Grupo 1", "Victor": "Grupo 1", "Kharla": "Grupo 1",
    "Renan": "Grupo 2", "Fabio": "Grupo 2", "Tio Israel": "Grupo 2", "Tia Socorro": "Grupo 2",
    "Constantino": "Grupo 3", "Juliane": "Grupo 3", "Tino": "Grupo 3"
}

# --- INICIALIZAÇÃO ---
if 'palpites' not in st.session_state: st.session_state.palpites = pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
if 'jogos' not in st.session_state: st.session_state.jogos = {}
if 'user_group' not in st.session_state: st.session_state.user_group = None
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

st.title("⚽ Bolão da Família - Copa 2026")

# --- LOGIN POR GRUPO / ADMIN ---
with st.sidebar:
    st.header("🔐 Login")
    if not st.session_state.user_group and not st.session_state.is_admin:
        login_tipo = st.radio("Tipo de Acesso:", ["Membro de Grupo", "Administrador"])
        
        if login_tipo == "Administrador":
            senha_adm = st.text_input("Senha Admin", type="password")
            if st.button("Entrar Admin"):
                if senha_adm == "davi2203": st.session_state.is_admin = True; st.rerun()
        else:
            grupo_sel = st.selectbox("Selecione seu Grupo:", ["Grupo 1", "Grupo 2", "Grupo 3"])
            senha_gp = st.text_input("Senha do Grupo", type="password")
            if st.button("Entrar"):
                senhas = {"Grupo 1": "vitones", "Grupo 2": "raelzinho", "Grupo 3": "tininho"}
                if senha_gp == senhas[grupo_sel]: st.session_state.user_group = grupo_sel; st.rerun()
    else:
        if st.button("Sair"): st.session_state.user_group = None; st.session_state.is_admin = False; st.rerun()

# --- PAINEL ADMIN (DAVI) ---
if st.session_state.is_admin:
    st.subheader("🛠️ Ferramentas do Davi")
    # ... (mesmo código de gerenciamento de jogos e ajuste de pontos de antes)
    # Adicione aqui as funções de deletar jogo e ajustar ranking do código anterior

# --- PALPITES (APENAS MEMBROS LOGADOS) ---
if st.session_state.user_group:
    st.subheader(f"📝 Registrar Palpite - {st.session_state.user_group}")
    membros = [n for n, g in participantes_db.items() if g == st.session_state.user_group]
    
    with st.form("palpite_form"):
        nome = st.selectbox("Quem é você?", membros)
        jogos_abertos = [j for j, s in st.session_state.jogos.items() if s == "Aberto"]
        jogo = st.selectbox("Qual jogo?", jogos_abertos) if jogos_abertos else st.error("Nenhum jogo aberto")
        palpite = st.text_input("Placar (ex: 2x1)")
        
        if st.form_submit_button("Enviar"):
            nova_linha = {"Nome": nome, "Grupo": st.session_state.user_group, "Jogo": jogo, "Palpite": palpite, "Pontos": 0}
            st.session_state.palpites = pd.concat([st.session_state.palpites, pd.DataFrame([nova_linha])], ignore_index=True)
            st.success("Palpite enviado!")

# --- CLASSIFICAÇÃO (VISÍVEL PARA TODOS) ---
st.subheader("📊 Classificação Geral")
if not st.session_state.palpites.empty:
    st.table(st.session_state.palpites.groupby("Nome")["Pontos"].sum().sort_values(ascending=False))
