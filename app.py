import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Bolão Davi Admin", layout="wide")

# --- BANCO DE DADOS (ARQUIVO ÚNICO) ---
DB_FILE = "bolao_total.csv"

def carregar_dados():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])

def salvar_dados(df):
    df.to_csv(DB_FILE, index=False)

if 'df' not in st.session_state: st.session_state.df = carregar_dados()
if 'jogos' not in st.session_state: st.session_state.jogos = []

# --- PAINEL DE CONTROLE (SÓ O DAVI MANDA) ---
st.title("⚙️ Painel de Controle Total do Davi")
senha = st.text_input("Senha Master:", type="password")

if senha == "davi2203":
    st.success("Controle Total Ativado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛠️ Gestão de Jogos")
        novo_j = st.text_input("Nome do Jogo:")
        if st.button("Adicionar Jogo"): st.session_state.jogos.append(novo_j)
        if st.button("Remover Jogo"): st.session_state.jogos.pop() if st.session_state.jogos else None
        st.write("Jogos Atuais:", st.session_state.jogos)

    with col2:
        st.subheader("📊 Gestão de Dados")
        if st.button("Resetar Tabela de Palpites"):
            st.session_state.df = pd.DataFrame(columns=["Nome", "Grupo", "Jogo", "Palpite", "Pontos"])
            salvar_dados(st.session_state.df)
            st.rerun()
            
    st.subheader("✏️ Editor de Palpites (Edite qualquer linha)")
    df_editor = st.data_editor(st.session_state.df, num_rows="dynamic")
    if st.button("Salvar Edições na Tabela"):
        st.session_state.df = df_editor
        salvar_dados(st.session_state.df)
        st.rerun()

else:
    st.warning("Insira a senha master para liberar o controle total.")

# --- VISUALIZAÇÃO PÚBLICA (OU PARA O DAVI) ---
st.markdown("---")
st.subheader("📜 Classificação e Histórico")
st.table(st.session_state.df.sort_values(by="Pontos", ascending=False))
