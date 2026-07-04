import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Bolão da Família 2026", layout="wide")

# --- INICIALIZAÇÃO DE ESTADO ---
if 'palpites' not in st.session_state:
    st.session_state.palpites = pd.DataFrame(columns=["Nome", "Jogo", "Palpite", "Pontos"])
if 'jogos' not in st.session_state:
    st.session_state.jogos = {}  # Formato: {"Brasil x Argentina": "Aberto"}
if 'resultados' not in st.session_state:
    st.session_state.resultados = {}  # Formato: {"Brasil x Argentina": "2x1"}
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
    
    # Criar Jogo
    novo_jogo = st.text_input("Novo Jogo (ex: Brasil x Argentina)")
    if st.button("Adicionar Jogo"):
        st.session_state.jogos[novo_jogo] = "Aberto"
        st.rerun()

    # Gerir Status e Resultado
    if st.session_state.jogos:
        jogo_sel = st.selectbox("Selecione o Jogo:", list(st.session_state.jogos.keys()))
        status_novo = st.radio("Status do Jogo:", ["Aberto", "Em Andamento", "Encerrado"], 
                               index=["Aberto", "Em Andamento", "Encerrado"].index(st.session_state.jogos[jogo_sel]))
        
        placar_real = st.text_input("Placar Oficial (Definir ao Encerrar):", value=st.session_state.resultados.get(jogo_sel, ""))
        
        if st.button("Salvar Alterações"):
            st.session_state.jogos[jogo_sel] = status_novo
            st.session_state.resultados[jogo_sel] = placar_real
            
            # Se for encerrado, calcula os pontos
            if status_novo == "Encerrado":
                mask = st.session_state.palpites["Jogo"] == jogo_sel
                for idx, row in st.session_state.palpites[mask].iterrows():
                    # Regras de Pontuação
                    if row["Palpite"] == placar_real:
                        pts = 5
                    elif "vitoria" in row["Palpite"].lower() or "vence" in row["Palpite"].lower(): # Exemplo de lógica
                        pts = 3
                    else:
                        pts = -3
                    
                    # Regra: se >= 50, perde 3 extra, nunca abaixo de 0
                    atual = st.session_state.palpites.at[idx, "Pontos"]
                    novo = atual + pts
                    if atual >= 50 and pts == -3: novo -= 3
                    st.session_state.palpites.at[idx, "Pontos"] = max(0, novo)
            st.success("Configurações salvas e pontos recalculados!")

# --- REGISTRO DE PALPITES (FAMÍLIA) ---
st.subheader("📝 Registrar Palpite")
jogos_abertos = [j for j, s in st.session_state.jogos.items() if s == "Aberto"]

if jogos_abertos:
    with st.form("form_palpite", clear_on_submit=True):
        nome = st.selectbox("Quem é você?", ["Davi", "Arthur", "Victor", "Kharla", "Renan", "Fabio", "Tio Israel", "Tia Socorro", "Constantino", "Juliane", "Tino"])
        jogo = st.selectbox("Qual jogo?", jogos_abertos)
        palpite = st.text_input("Seu placar (ex: 2x1)")
        
        if st.form_submit_button("Enviar Palpite"):
            # Trava de segurança (já votou?)
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
col1, col2 = st.columns(2)

with col1:
    st.subheader("📜 Histórico de Palpites")
    st.table(st.session_state.palpites[["Nome", "Jogo", "Palpite"]])

with col2:
    st.subheader("📊 Classificação")
    if not st.session_state.palpites.empty:
        rank = st.session_state.palpites.groupby("Nome")["Pontos"].sum().reset_index()
        rank = rank.sort_values(by="Pontos", ascending=False).reset_index(drop=True)
        rank.index = rank.index + 1
        st.table(rank)
    else:
        st.write("Ranking vazio.")

st.subheader("📍 Status dos Jogos")
st.write(pd.DataFrame(list(st.session_state.jogos.items()), columns=["Jogo", "Status"]))
