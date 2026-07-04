import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Bolão da Família - 2026", layout="wide")

# Inicialização dos estados
if 'palpites' not in st.session_state:
    st.session_state.palpites = pd.DataFrame(columns=["Nome", "Jogo", "Palpite", "Pontos"])
if 'jogos_ativos' not in st.session_state:
    st.session_state.jogos_ativos = []
if 'resultados_oficiais' not in st.session_state:
    st.session_state.resultados_oficiais = {}

st.title("⚽ Bolão da Família - Copa do Mundo 2026")

# --- LOGIN DO ADMIN (DAVI) ---
st.sidebar.header("🔐 Área do Administrador")
senha = st.sidebar.text_input("Senha do Davi", type="password")

if senha == "davi2203":
    st.sidebar.success("Logado como Davi (Admin)")
    st.subheader("🛠️ Painel de Controle do Davi")
    
    # Gerenciar Jogos
    col1, col2 = st.columns(2)
    with col1:
        novo_jogo = st.text_input("Adicionar novo jogo (ex: Brasil x Argentina)")
        if st.button("Adicionar Jogo"):
            if novo_jogo not in st.session_state.jogos_ativos:
                st.session_state.jogos_ativos.append(novo_jogo)
                st.rerun()
    with col2:
        remover = st.selectbox("Remover jogo:", st.session_state.jogos_ativos)
        if st.button("Remover Jogo"):
            st.session_state.jogos_ativos.remove(remover)
            st.rerun()

    # Definir/Editar Resultados
    st.markdown("---")
    st.subheader("🏁 Definir ou Editar Resultados")
    jogo_apurar = st.selectbox("Selecione o jogo para dar o placar:", st.session_state.jogos_ativos)
    placar_oficial = st.text_input("Placar oficial (ex: 2x1)", value=st.session_state.resultados_oficiais.get(jogo_apurar, ""))
    
    if st.button("Salvar e Recalcular Pontos"):
        st.session_state.resultados_oficiais[jogo_apurar] = placar_oficial
        
        # Resetar pontos para recalcular
        st.session_state.palpites["Pontos"] = 0
        
        # Recálculo total
        for jogo, resultado in st.session_state.resultados_oficiais.items():
            mask = st.session_state.palpites["Jogo"] == jogo
            for index, row in st.session_state.palpites[mask].iterrows():
                # Lógica de pontos
                if row["Palpite"] == resultado:
                    pts = 5
                elif "ganhou" in row["Palpite"] or "perdeu" in row["Palpite"]:
                    pts = 3
                else:
                    pts = -3
                
                # Regra de penalidade (se >= 50 pontos)
                pts_atuais = st.session_state.palpites.at[index, "Pontos"]
                novo_total = pts_atuais + pts
                
                # Aplica desconto se já tinha 50+
                if pts_atuais >= 50 and pts == -3:
                    novo_total -= 3
                
                st.session_state.palpites.at[index, "Pontos"] = max(0, novo_total)
        st.success("Placar salvo e pontuação recalculada!")

# --- REGISTRO DE PALPITES (FAMÍLIA) ---
st.subheader("📝 Registre seu Palpite")
with st.form("form_palpite"):
    nome = st.selectbox("Quem é você?", ["Davi", "Arthur", "Victor", "Kharla", "Renan", "Fabio", "Tio Israel", "Tia Socorro", "Constantino", "Juliane", "Tino"])
    jogo = st.selectbox("Qual jogo?", st.session_state.jogos_ativos)
    palpite = st.text_input("Seu palpite (ex: 2x1)")
    
    if st.form_submit_button("Enviar Palpite"):
        if jogo and palpite:
            nova_linha = {"Nome": nome, "Jogo": jogo, "Palpite": palpite, "Pontos": 0}
            st.session_state.palpites = pd.concat([st.session_state.palpites, pd.DataFrame([nova_linha])], ignore_index=True)
            st.success(f"Palpite de {nome} para {jogo} registrado!")
        else:
            st.error("Preencha o jogo e o palpite!")

# --- RANKING ---
st.subheader("📊 Ranking do Bolão")
if not st.session_state.palpites.empty:
    ranking = st.session_state.palpites.groupby("Nome")["Pontos"].sum().reset_index()
    ranking = ranking.sort_values(by="Pontos", ascending=False)
    st.table(ranking)
else:
    st.info("Nenhum palpite registrado ainda.")
