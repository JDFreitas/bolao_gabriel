import streamlit as st
import pandas as pd

@st.cache_data
def carregar_dados():
    # Carregando a tabela de palpites do arquivo excel
    palpites = pd.read_csv("database/palpites.csv")
    # Carregando a tabela de resultados do arquivo excel
    resultados = pd.read_csv("database/resultados_brasileirao.csv")

    # Criando coluna de jogo_completo para facilitar a comparação
    # Concatenando as colunas Mandante e Visitante da tabela palpites
    palpites['jogo_completo'] = palpites['Mandante'] + palpites['Visitante']
    # Removendo os espaços da coluna jogo_completo da tabela palpites
    palpites['jogo_completo'] = palpites['jogo_completo'].str.replace(' ', '')
    

    # Concatenando as colunas Mandante e Visitante da tabela resultados
    resultados['jogo_completo'] = resultados['Mandante'] + resultados['Visitante']
    # Removendo os espaços da coluna jogo_completo da tabela resultados
    resultados['jogo_completo'] = resultados['jogo_completo'].str.replace(' ', '')
    
    # Retornando as tabelas palpites e resultados tratadas
    return palpites, resultados


if "palpites" not in st.session_state:
    st.session_state["palpites"], st.session_state["resultados"] = carregar_dados()           
    
st.title("BOLÃO DOS AMIGOS DE 2025 ⚽")

st.divider()

col1, col2, col3 = st.columns([0.4,0.1,0.4])

with col1:
    st.subheader("Regras do Bolão")
    st.markdown("""
        1) Os palpites deverão ser dados antes do início do Campeonato Brasileiro Série A para todos os jogos, no total serão 380 jogos.
        2) O valor do Bolão deverá ser pago para o Administrador antes do início do Campeonato.
        3) A premiação será dada da seguinte forma:
            - **1º Lugar** = 50% do valor arrecadado
            - **2º Lugar** = 30% do valor arrecadado
            - **3º Lugar** = 20% do valor arrecadado
        
        4) Será descontado do valor da premiação acima a taxa de administrador abaixo:
                - **Taxa Adm:** 0%
    """)

with col2:
    st.html(
        '''
        <div class="divider-vertical-line"></div>
        <style>
            .divider-vertical-line {
                border-left: 2px solid rgba(49, 51, 63);
                height: 500px;
                margin: auto;
            }
        </style>
        '''
        )


with col3:
    st.subheader("Pontuação:")
    st.markdown("**5** - Acertar o Resultado Exato")
    st.markdown("**3** - Acertar o resultado")
    st.markdown("**0** - Nenhum acima")
    st.subheader("**Pontuação Extra:**")
    st.markdown("**2x** Acertar o Jogo coringa")