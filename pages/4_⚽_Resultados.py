# Bibliotecas
import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup


def atualizar_resultados_brasileirao(rodada, resultados_brasileirao="database/resultados_brasileirao.csv"):
    """
    Recebe o número da rodada, lê o arquivo de resultados, faz a requisição dos valores
    e atualiza o arquivo CSV com os novos resultados, se necessário.
    Retorna o DataFrame com os resultados da rodada.
    """
    # Garante que a rodada seja string
    rodada = str(rodada)

    
    df_brasileirao = pd.read_csv(resultados_brasileirao)
    

    # Se já existe a rodada no arquivo, retorna os dados dela
    if not df_brasileirao.empty and rodada in df_brasileirao['Rodada'].astype(str).values:
        df_brasileirao = df_brasileirao[df_brasileirao['Rodada'].astype(str) != rodada]
       

    # Caso contrário, faz a requisição dos resultados
    url = f"https://www.api-futebol.com.br/campeonato/campeonato-brasileiro/2025/rodada/{rodada}?stageSlug=fase-unica-campeonato-brasileiro-2025"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        class_p1 = soup.find_all(class_='p-1')

        resultados = []
        for elemento in class_p1:
            class_p0 = elemento.find_all(class_='p-0')
            if len(class_p0) > 0:
                mandante = class_p0[0].text.replace("\n", "")
                placar = class_p0[1].text.replace("\n", "")
                visitante = class_p0[2].text.replace("\n", "")
                resultados.append({"Rodada": rodada, "Mandante": mandante, "Placar": placar, "Visitante": visitante})

        df = pd.DataFrame(resultados)

        df_brasileirao = pd.concat([df_brasileirao, df], ignore_index=True)

        df_brasileirao.to_csv(resultados_brasileirao, index=False)
    else:
        raise Exception("Não foi possível buscar os resultados. Verifique a URL ou tente novamente mais tarde.")
    

# Configuração do Streamlit
st.title("Resultados do Campeonato Brasileiro 2025")

# Entrada do usuário para a rodada
rodada = st.number_input("Digite a rodada:", min_value=1, max_value=38, value=7, step=1)

df_resultados = st.session_state["resultados"]
df = df_resultados[df_resultados['Rodada'].astype(str) == str(rodada)]
st.dataframe(df.drop(columns=["Rodada"]), use_container_width=True, hide_index=True)

criar_rodada = st.button("Atualizar Resultados da Rodada")

if criar_rodada:
    atualizar_resultados_brasileirao(rodada)
    st.rerun() # Usar st.rerun()




    
