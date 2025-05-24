import streamlit as st
import pandas as pd

df_palpites = st.session_state["palpites"]
# Obtendo lista única de jogadores
jogadores = df_palpites["Jogador"].unique()

# Criando DataFrame com informações dos jogadores
df_jogadores = pd.DataFrame({
    "Jogador": jogadores,
    "Acertos": 0,
    "Adm": False,
    "Valores": 100,
    "Status_Pagamento": "Pendente"
})

df_jogadores