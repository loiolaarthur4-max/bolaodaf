import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Bolão da Família 2026", layout="wide")

# --- BANCO DE DADOS ---
participantes_db = {
    "Davi": "Grupo 1", "Arthur": "Grupo 1", "Victor": "Grupo 1", "Kharla": "Grupo 1",
    "Renan": "Grupo 2", "Fabio": "Grupo 2", "Tio Israel": "Grupo 2", "Tia Socorro": "Grupo 2",
    "Constantino": "Grupo 3", "Juliane": "Grupo 3", "Tino": "Grupo 3"
}

# --- INICIALIZAÇÃO ---
if 'palpites' not in st.session_state: 
    st.session_state.palpites = pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
if 'jogos' not in st.session_state: st.session_state.jogos = {}
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

st.title("⚽ Bolão da Família - Copa 2026")

# --- LOGIN ADMIN ---
with st.sidebar:
    st.header("🔐 Área do Administrador")
    if not st.session_state.logged_in:
        senha = st.text_input("Senha do Davi", type="password")
        if st.button("Entrar"):
            if senha == "davi2203": st.session_state.logged_in = True; st.rerun()
    else:
        if st.button("Sair da Conta"): st.session_state.logged_in = False; st.rerun()

# --- PAINEL DO ADMIN ---
if st.session_state.logged_in:
    st.subheader("🛠️ Ferramentas do Davi")
    tab1, tab2, tab3 = st.tabs(["Jogos", "Ajustar Ranking", "Logs"])
    
    with tab1:
        novo_jogo = st.text_input("Nome do novo Jogo")
        if st.button("Adicionar Jogo"): st.session_state.jogos[novo_jogo] = "Aberto"; st.rerun()
        
        jogo_del = st.selectbox("Remover Jogo", list(st.session_state.jogos.keys()) + [""])
        if st.button("Deletar Jogo"): 
            del st.session_state.jogos[jogo_del]
            st.session_state.palpites = st.session_state.palpites[st.session_state.palpites["Jogo"] != jogo_del]
            st.rerun()
            
    with tab2:
        nome_ajuste = st.selectbox("Quem ajustar?", list(participantes_db.keys()))
        pontos_ajuste = st.number_input("Definir total de pontos manualmente:", value=0)
        if st.button("Atualizar Pontuação"):
            # Ajusta o primeiro palpite encontrado do usuário para refletir os pontos totais
            st.session_state.palpites.loc[st.session_state.palpites["Nome"] == nome_ajuste, "Pontos"] = 0
            idx = st.session_state.palpites[st.session_state.palpites["Nome"] == nome_ajuste].index[0]
            st.session_state.palpites.at[idx, "Pontos"] = pontos_ajuste
            st.rerun()

# --- PALPITES (FAMÍLIA) ---
st.subheader("📝 Registrar Palpite")
with st.form("palpite_form"):
    nome = st.selectbox("Participante", list(participantes_db.keys()))
    jogos_abertos = [j for j, s in st.session_state.jogos.items() if s == "Aberto"]
    jogo = st.selectbox("Jogo", jogos_abertos)
    palpite = st.text_input("Placar (ex: 2x1)")
    if st.form_submit_button("Enviar Palpite"):
        nova_linha = {"Nome": nome, "Grupo": participantes_db[nome], "Jogo": jogo, "Palpite": palpite, "Pontos": 0}
        st.session_state.palpites = pd.concat([st.session_state.palpites, pd.DataFrame([nova_linha])], ignore_index=True)
        st.rerun()

# --- HISTÓRICO E CLASSIFICAÇÃO ---
col_h, col_r = st.columns(2)

with col_h:
    st.subheader("📜 Histórico")
    for i, row in st.session_state.palpites.iterrows():
        c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
        c1.write(row["Nome"]); c2.write(row["Jogo"]); c3.write(row["Palpite"])
        if st.session_state.logged_in:
            if c4.button("🗑️", key=f"del_{i}"):
                st.session_state.palpites = st.session_state.palpites.drop(i)
                st.rerun()

with col_r:
    st.subheader("📊 Classificação")
    if not st.session_state.palpites.empty:
        rank = st.session_state.palpites.groupby("Nome")["Pontos"].sum().sort_values(ascending=False).reset_index()
        rank.index = rank.index + 1
        st.table(rank)
    else:
        st.write("Nenhum palpite registrado.")
