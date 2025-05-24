import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Tabela de Pontuação - Bolão",
    page_icon="⚽",
    layout="wide"
)

# Título da aplicação
st.title("🏆 Tabela de Pontuação do Bolão")

# Função para determinar o resultado do jogo
def determinar_resultado(placar):
    # Verifica se o jogo ainda não foi realizado (placar = 'x')
    if placar == 'x':  # Jogo não realizado
        return None
    
    # Divide o placar em gols do mandante e visitante usando o 'x' como separador
    gols = placar.split('x')
    # Converte os gols do mandante para inteiro removendo espaços
    gols_mandante = int(gols[0].strip())
    # Converte os gols do visitante para inteiro removendo espaços
    gols_visitante = int(gols[1].strip())
    
    # Verifica se o mandante fez mais gols
    if gols_mandante > gols_visitante:
        return 'mandante'
    # Verifica se o visitante fez mais gols
    elif gols_mandante < gols_visitante:
        return 'visitante'
    # Se nenhuma condição anterior for verdadeira, é empate
    else:
        return 'empate'

# Função para calcular pontos do palpite
def calcular_pontos(palpite, resultado):
    # Verifica se o jogo ainda não foi realizado (placar = 'x')
    if resultado['Placar'] == 'x':  # Jogo não realizado
        return 0
    
    # Verifica se acertou o placar exato
    if palpite['Placar'] == resultado['Placar']:
        # Se acertou o placar exato, ganha 5 pontos
        pontos = 5
    else:
        # Obtém o resultado (vitória/empate) do palpite
        resultado_palpite = determinar_resultado(palpite['Placar'])
        # Obtém o resultado real do jogo
        resultado_real = determinar_resultado(resultado['Placar'])
        
        # Verifica se acertou pelo menos o resultado
        if resultado_palpite == resultado_real:
            # Se acertou só o resultado, ganha 3 pontos
            pontos = 3
        else:
            # Se errou tudo, não ganha pontos
            pontos = 0
    # Verifica se o palpite foi marcado como coringa
    if palpite['Coringa'] == 'SIM':
        # Se for coringa, dobra os pontos
        pontos *= 2
    # Retorna a pontuação final do palpite
    return pontos

# Função para calcular pontuação por rodada
def calcular_pontuacao_rodada(rodada=None):
    # Criando o dataframe para a Pontuação com as colunas (Jogador, Pontos)
    pontuacao = pd.DataFrame(columns=['Jogador', 'Pontos'])
    # Listando os jogadores
    jogadores = palpites['Jogador'].unique()
    
    # Paracada Jogador em Jogadores
    for jogador in jogadores:
        # Zerando as pontuação
        pontos_jogador = 0
        # Criando um dataframe com os palpetes do jogador filtrando da tabela palpites quando a coluna jogador for igual a jogador
        palpites_jogador = palpites[palpites['Jogador'] == jogador]
        # se não for none e diferente de "Todas"
        if rodada and rodada != "Todas":
            # Aplicando mais um filtro na tabela dos palpites do jogador caso a rodada seja a rodada selecionda
            palpites_jogador = palpites_jogador[palpites_jogador['Rodada'] == int(rodada)]
        # Para cada index, e linha da tabela palpite_jogador (_ ignorando o index)
        for _, palpite in palpites_jogador.iterrows():
            # Filtrando a tabela resultados pela coluna jogo_completo com base na tabela palpites_Jogador coluna jogo_completo
            resultado = resultados[resultados['jogo_completo'] == palpite['jogo_completo']]
            # Se a tabela resultado não estiver vazia
            if not resultado.empty:
                # chamda da função calcular_pontos com a Tabela com a linha do jogo encontrado
                pontos = calcular_pontos(palpite, resultado.iloc[0])
                # Acrescentando os pontos ao Jogador
                pontos_jogador += pontos
        # Adicionando a linha do jogador a tabela pontuação
        pontuacao = pd.concat([pontuacao, pd.DataFrame({'Jogador': [jogador], 'Pontos': [pontos_jogador]})], ignore_index=True)
    # Retornando a tabela pontuação em ordem descrescente pela coluna pontos
    return pontuacao.sort_values('Pontos', ascending=False)

    
palpites, resultados = st.session_state["palpites"], st.session_state["resultados"]

# Sidebar para filtros com cabeçalho filtros
st.sidebar.header("Filtros")

# Filtro por rodada
rodadas = sorted(palpites['Rodada'].unique())
# Lista do Selectebox na sidebar
rodada_selecionada = st.sidebar.selectbox(
    "Selecione a Rodada",
    ["Todas"] + list(map(str, rodadas))
)

########### Calculando pontuação com base no filtro #########
if rodada_selecionada == "Todas": 
    pontuacao = calcular_pontuacao_rodada()
    st.subheader("Pontuação Geral")
else:
    pontuacao = calcular_pontuacao_rodada(rodada_selecionada)
    st.subheader(f"Pontuação da Rodada {rodada_selecionada}")

# Adicionando estatísticas
col1, col2, col3 = st.columns(3)

with col1:
    # st.metric("Total de Jogadores", len(pontuacao))
    st.metric("Melhor da Rodada", f"{pontuacao.loc[pontuacao['Pontos'].idxmax(), 'Jogador']} {pontuacao['Pontos'].max()} 👍", border=True)
with col2:
    st.metric("Pior da Rodada", f"{pontuacao.loc[pontuacao['Pontos'].idxmin(), 'Jogador']} {pontuacao['Pontos'].min()} 👎",border=True)
with col3:
    st.metric("Total de Jogadores", len(pontuacao),border=True)


# Exibindo a tabela de pontuação
st.dataframe(
    pontuacao,
    column_config={
        "Jogador": st.column_config.TextColumn(
            "Jogador",
            width="medium",
        ),
        "Pontos": st.column_config.NumberColumn(
            "Pontos",
            width="small",
            format="%d ⭐",
        ),
    },
    hide_index=True,
)


# Adicionando um gráfico de barras
st.subheader("Gráfico de Pontuação")
st.bar_chart(pontuacao.set_index('Jogador')) 