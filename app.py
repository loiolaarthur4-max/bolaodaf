import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Bolão da Família 2026", layout="wide")

# --- INICIALIZAÇÃO DE ESTADO ---
if 'palpites' not in st.session_state:
    st.session_state.palpites = pd.DataFrame(columns=["Nome", "Jogo", "Palpite", "Pontos"])
if 'jogos' not in st.session_state:
    st.session_state.jogos = {}  # Formato: {"Jogo": "Status"}
if 'resultados' not in st.session_state:
    st.session_state.resultados = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.title("⚽ Bolão da Família - Copa 2026")

# --- PAINEL DO ADMIN (DAVI) ---
st.sidebar.header("🔐 Área do Administrador")
if not st.session_state.logged_in:
    senha = st.sidebar.text_input("Senha do Davi", type="password")
    if st.sidebar.button("Entrar"):
        if senha == "davi2203":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.sidebar.error("Senha incorreta!")
else:
    if st.sidebar.button("Sair da Conta"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.subheader("🛠️ Painel de Controle do Davi")
    
    # Adicionar Jogo
    novo_jogo = st.text_input("Adicionar novo jogo:")
    if st.button("Criar Jogo"):
        st.session_state.jogos[novo_jogo] = "Aberto"
        st.rerun()

    # Gerenciar Jogos Existentes
    if st.session_state.jogos:
        st.markdown("---")
        jogo_sel = st.selectbox("Gerenciar Jogo:", list(st.session_state.jogos.keys()))
        
        # Alterar Status
        status_novo = st.radio("Status:", ["Aberto", "Em Andamento", "Encerrado"], 
                               index=["Aberto", "Em Andamento", "Encerrado"].index(st.session_state.jogos[jogo_sel]))
        
        # Definir Resultado
        placar_real = st.text_input("Definir/Corrigir Placar Oficial:", value=st.session_state.resultados.get(jogo_sel, ""))
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Salvar Alterações e Recalcular"):
                st.session_state.jogos[jogo_sel] = status_novo
                st.session_state.resultados[jogo_sel] = placar_real
                
                # Recálculo de pontos
                if status_novo == "Encerrado":
                    mask = st.session_state.palpites["Jogo"] == jogo_sel
                    for idx, row in st.session_state.palpites[mask].iterrows():
                        if row["Palpite"] == placar_real:
                            pts = 5
                        elif "vence" in row["Palpite"].lower(): 
                            pts = 3
                        else:
                            pts = -3
                        
                        atual = st.session_state.palpites.at[idx, "Pontos"]
                        novo = atual + pts
                        if atual >= 50 and pts == -3: novo -= 3
                        st.session_state.palpites.at[idx, "Pontos"] = max(0, novo)
                st.success("Dados atualizados!")
                st.rerun()
        
        with col_btn2:
            if st.button("EXCLUIR JOGO DEFINITIVAMENTE"):
                del st.session_state.jogos[jogo_sel]
                if jogo_sel in st.session_state.resultados: del st.session_state.resultados[jogo_sel]
                st.session_state.palpites = st.session_state.palpites[st.session_state.palpites["Jogo"] != jogo_sel]
                st.rerun()

# --- REGISTRO DE PALPITES (FAMÍLIA) ---
st.subheader("📝 Registrar Palpite")
jogos_abertos = [j for j, s in st.session_state.jogos.items() if s == "Aberto"]

if jogos_abertos:
    with st.form("form_palpite", clear_on_submit=True):
        nome = st.selectbox("Quem é você?", ["Davi", "Arthur", "Victor", "Kharla", "Renan", "Fabio", "Tio Israel", "Tia Socorro", "Constantino", "Juliane", "Tino"])
        jogo = st.selectbox("Qual jogo?", jogos_abertos)
        palpite = st.text_input("Seu placar (ex: 2x1)")
        
        if st.form_submit_button("Enviar Palpite"):
            ja_votou = ((st.session_state.palpites["Nome"] == nome) & (st.session_state.palpites["Jogo"] == jogo)).any()
            if ja_votou:
                st.error("❌ Você já palpitou neste jogo! Não é permitido alterar.")
            else:
                nova_linha = {"Nome": nome, "Jogo": jogo, "Palpite": palpite, "Pontos": 0}
                st.session_state.palpites = pd.concat([st.session_state.palpites, pd.DataFrame([nova_linha])], ignore_index=True)
                st.success("✅ Palpite registrado!")
else:
    st.info("Não há jogos abertos para palpites no momento.")

# --- VISUALIZAÇÃO ---
col_v1, col_v2 = st.columns(2)

with col_v1:
    st.subheader("📜 Histórico")
    st.table(st.session_state.palpites[["Nome", "Jogo", "Palpite", "Pontos"]])

with col_v2:
    st.subheader("📊 Classificação")
    if not st.session_state.palpites.empty:
        rank = st.session_state.palpites.groupby("Nome")["Pontos"].sum().reset_index()
        rank = rank.sort_values(by="Pontos", ascending=False).reset_index(drop=True)
        rank.index = rank.index + 1
        st.table(rank)
    else:
        st.write("Ranking vazio.")

st.markdown("---")
st.subheader("📍 Status dos Jogos")
st.table(pd.DataFrame(list(st.session_state.jogos.items()), columns=["Jogo", "Status"]))
