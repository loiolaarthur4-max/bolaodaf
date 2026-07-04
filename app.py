import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Bolão da Família", layout="wide")

# Inicialização do estado
if 'palpites' not in st.session_state:
    st.session_state.palpites = pd.DataFrame(columns=["Nome", "Jogo", "Palpite", "Pontos"])
if 'jogos_ativos' not in st.session_state:
    st.session_state.jogos_ativos = []

st.title("⚽ Bolão da Família - Copa 2026")

# Login de Administrador
st.sidebar.header("🔐 Acesso do Administrador")
senha = st.sidebar.text_input("Senha do Davi", type="password")

if senha == "davi2203":
    st.sidebar.success("Logado como Davi (Admin)")
    
    # Gerenciamento de Jogos
    st.subheader("🛠️ Painel do Administrador")
    col1, col2 = st.columns(2)
    
    with col1:
        novo_jogo = st.text_input("Adicionar novo jogo (ex: Brasil x Alemanha)")
        if st.button("Adicionar Jogo"):
            if novo_jogo not in st.session_state.jogos_ativos:
                st.session_state.jogos_ativos.append(novo_jogo)
    
    with col2:
        jogo_remover = st.selectbox("Remover jogo:", st.session_state.jogos_ativos)
        if st.button("Remover Jogo"):
            st.session_state.jogos_ativos.remove(jogo_remover)
            st.rerun()

    # Definir Resultado Real
    st.subheader("🏁 Definir Resultado Real")
    if st.session_state.jogos_ativos:
        jogo_apurar = st.selectbox("Selecione o jogo para dar o placar:", st.session_state.jogos_ativos)
        placar_real = st.text_input("Placar oficial (ex: 2x1)")
        
        if st.button("Calcular Pontuação Final"):
            # Lógica de cálculo
            mask = st.session_state.palpites["Jogo"] == jogo_apurar
            for index, row in st.session_state.palpites[mask].iterrows():
                if row["Palpite"] == placar_real:
                    pontos = 5
                elif "ganhou" in row["Palpite"] or "perdeu" in row["Palpite"]:
                    pontos = 3
                else:
                    pontos = -3
                
                # Regra: pontos >= 50 perde 3, nunca menor que 0
                total = st.session_state.palpites.at[index, "Pontos"] + pontos
                st.session_state.palpites.at[index, "Pontos"] = max(0, total)
            st.success(f"Pontos para {jogo_apurar} calculados!")
else:
    st.sidebar.info("Apenas o Davi pode alterar os jogos e resultados.")

# Registro de palpites (Aberto para todos)
st.subheader("📝 Registrar seu Palpite")
with st.form("form_palpite"):
    nome = st.selectbox("Quem é você?", ["Davi", "Arthur", "Victor", "Kharla", "Renan", "Fabio", "Tio Israel", "Tia Socorro", "Constantino", "Juliane", "Tino"])
    jogo = st.selectbox("Qual jogo?", st.session_state.jogos_ativos)
    palpite = st.text_input("Seu palpite (ex: 2x1)")
    if st.form_submit_button("Enviar Palpite"):
        nova_linha = {"Nome": nome, "Jogo": jogo, "Palpite": palpite, "Pontos": 0}
        st.session_state.palpites = pd.concat([st.session_state.palpites, pd.DataFrame([nova_linha])], ignore_index=True)
        st.success("Palpite registrado!")

# Ranking
st.subheader("📊 Ranking Geral")
st.table(st.session_state.palpites.groupby("Nome")["Pontos"].sum().sort_values(ascending=False))
