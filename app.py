import streamlit as st
import pandas as pd

st.title("⚽ Bolão da Família - Copa 2026")

# Inicialização do estado
if 'palpites' not in st.session_state:
    st.session_state.palpites = pd.DataFrame(columns=["Nome", "Jogo", "Palpite", "Pontos"])

# 1. Registrar Palpite
st.subheader("📝 Registrar Palpite")
with st.form("form_palpite"):
    nome = st.selectbox("Quem está palpitando?", ["Davi", "Arthur", "Victor", "Kharla", "Renan", "Fabio", "Tio Israel", "Tia Socorro", "Constantino", "Juliane", "Tino"])
    jogo = st.text_input("Nome do Jogo (ex: Brasil x Argentina)")
    palpite = st.text_input("Placar (ex: 2x1)")
    btn_enviar = st.form_submit_button("Registrar Palpite")

    if btn_enviar:
        nova_linha = {"Nome": nome, "Jogo": jogo, "Palpite": palpite, "Pontos": 0}
        st.session_state.palpites = pd.concat([st.session_state.palpites, pd.DataFrame([nova_linha])], ignore_index=True)
        st.success(f"Palpite de {nome} para {jogo} registrado!")

# 2. Apuração (Só libera pontos se houver palpite registrado)
st.subheader("🏁 Apurar Jogo")
if not st.session_state.palpites.empty:
    jogo_selecionado = st.selectbox("Selecione o jogo para apurar:", st.session_state.palpites["Jogo"].unique())
    resultado_real = st.text_input("Resultado Final do Jogo (ex: 1x1)")
    
    if st.button("Calcular Pontos"):
        # Filtra palpites desse jogo
        mask = st.session_state.palpites["Jogo"] == jogo_selecionado
        for index, row in st.session_state.palpites[mask].iterrows():
            # Regras de cálculo
            if row["Palpite"] == resultado_real:
                pontos = 5
            elif "ganhou" in row["Palpite"] or "perdeu" in row["Palpite"]: # Lógica simples
                pontos = 3
            else:
                pontos = -3
            
            # Aplica regra de não ficar negativo (exemplo básico)
            st.session_state.palpites.at[index, "Pontos"] = max(0, pontos)
        st.success("Pontos calculados!")
else:
    st.warning("Nenhum palpite registrado ainda.")

# 3. Exibir Tabela de Pontos
st.subheader("📊 Placar Atualizado")
st.table(st.session_state.palpites)
