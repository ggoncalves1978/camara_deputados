## Bibliotecas
import pandas as pd
from babel.numbers import format_currency
import os
import warnings
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=pd.errors.DtypeWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

#-----------------------------------------------------------------------------------------------------------------#
## Configurações

# Ajuste configuração de pagina
st.set_page_config(
    layout="wide",
    page_title="Portal | Câmara dos Deputados",
    page_icon= ':classical_building:')

st.markdown(
    """
    <style>
    .Balança_Comercial {
        background-color: #F5F5F5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# load Style css
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#-----------------------------------------------------------------------------------------------------------------#
# Caminho onde estão os datasets
caminho_despesas = './app_web/Despesas_final.parquet'

#-----------------------------------------------------------------------------------------------------------------#
# Utilizado para operações pesadas
@st.cache_data
def load_data(caminho):
    df = pd.read_parquet(caminho)
    return df

# Carregar e armazenar dados no session_state se ainda não estiverem lá
if "df_despesas" not in st.session_state:
    st.session_state["df_despesas"] = load_data(caminho_despesas)

# Acessar os dados do session_state
df_despesas = st.session_state["df_despesas"]
df_despesas_2 = st.session_state["df_despesas"]
df_despesas_3 = st.session_state["df_despesas"]

ano_menor = df_despesas['Ano'].min()
ano_maior = df_despesas['Ano'].max()

#-----------------------------------------------------------------------------------------------------------------#
# Sidebar

# Adicionar a opção "Todos os Anos" à lista de anos
ano = ["Todos"] + df_despesas['Ano'].unique().tolist()
partido = ['Todos'] + df_despesas['Partido'].unique().tolist()


st.sidebar.header('Filtros')
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", ano)

# Filtrar o DataFrame Principal - Ano
if ano_selecionado == "Todos":
    df_despesas_filtered = df_despesas
else:
    df_despesas_filtered = df_despesas[df_despesas['Ano'].isin([ano_selecionado])]

if ano_selecionado == "Todos":
    df_despesas_filtered_2 = df_despesas_2
else:
    df_despesas_filtered_2 = df_despesas_2[df_despesas_2['Ano'].isin([ano_selecionado])]

if ano_selecionado == "Todos":
    df_despesas_filtered_3 = df_despesas_3
else:
    df_despesas_filtered_3 = df_despesas_3[df_despesas_3['Ano'].isin([ano_selecionado])]

# Filtrar Partidos
partido_selecionado = st.sidebar.selectbox('Selecione o partido', partido, placeholder="Digite nome do partido...")

# Filtrar o DataFrame Principal - Partido
if partido_selecionado != "Todos":
    df_despesas_filtered = df_despesas_filtered[df_despesas_filtered['Partido'] == partido_selecionado]

if partido_selecionado != "Todos":
    df_despesas_filtered_2 = df_despesas_filtered_2[df_despesas_filtered_2['Partido'] == partido_selecionado]

# Atualizar lista de deputados com base no partido selecionado
deputados = ['Todos'] + df_despesas_filtered['Nome_Parlamentar'].unique().tolist()
deputado_selecionado = st.sidebar.selectbox('Selecione o parlamentar', deputados, placeholder="Digite o nome do parlamentar...")

# Filtrar o DataFrame Principal - Deputado
if deputado_selecionado != "Todos":
    df_despesas_filtered = df_despesas_filtered[df_despesas_filtered['Nome_Parlamentar'] == deputado_selecionado]

st.sidebar.markdown("Desenvolvido por Gabriel Gonçalves")
st.sidebar.markdown('https://www.linkedin.com/in/gabrielgoncalves78/')

#-----------------------------------------------------------------------------------------------------------------#
# Graficos

# Extrair o menor / maior Ano do dataset
ano_inicial = df_despesas_filtered['Ano_Mes'].min()
ano_final = df_despesas_filtered['Ano_Mes'].max()

# Tabela de quantidade de deputados por partido
qtde_parlamentar = df_despesas_filtered.groupby(['Partido'])['Nome_Parlamentar'].nunique().sort_values(ascending=False).reset_index()

fig_qtde_parlamentar = px.bar(qtde_parlamentar, x="Partido", y="Nome_Parlamentar", title='Quantidade de deputados por partido')

# Gasto mensal por parlamentar
df_despesas_deputado_mes = df_despesas_filtered.groupby(['Ano_Mes', 'Nome_Parlamentar'])['Vlr_Liquido'].sum().reset_index()

fig_gastos_deput = px.line(df_despesas_deputado_mes,
                           x = 'Ano_Mes',
                           y = 'Vlr_Liquido')
                           
# Gasto mensal detalhado por tipo de despesa #'Ano_Mes', 'Nome_Parlamentar',
df_despesas_tipo_mes = df_despesas_filtered.groupby(['Descricao_txt'])['Vlr_Liquido'].sum().sort_values(ascending=False).reset_index()

fig_gastos_tipo = px.bar(df_despesas_tipo_mes,
                           x = 'Descricao_txt',
                           y = 'Vlr_Liquido')
# Alterando a cor de todas as barras para uma cor específica (ex: 'blue')
fig_gastos_tipo.update_traces(marker_color='yellow')
                           
# Gasto mensal por partido
df_despesas_partido_ano = df_despesas_filtered.groupby(['Ano_Mes','Partido'], as_index=False).agg({'Vlr_Liquido':'sum'}).reset_index()
                                                                                    
fig_gastos_partido = px.bar(df_despesas_partido_ano,
                           x = 'Partido',
                           y = 'Vlr_Liquido',
                           title= f'Gasto por partido no ano de {ano}')

# Gasto anual por partido e deputado
df_despesas_partido_deputado_ano = df_despesas_filtered_2.groupby(['Partido','Nome_Parlamentar'], as_index=False).agg(
                                                                {'Vlr_Liquido':'sum'}).sort_values(by='Vlr_Liquido',ascending=False).reset_index()

colunas = ['Nome_Parlamentar', 'Vlr_Liquido']
df_despesas_partido_deputado_ano_filtered = df_despesas_partido_deputado_ano[colunas]

fig_gastos_partido_dep = px.bar(df_despesas_partido_deputado_ano_filtered,
                                 x = 'Nome_Parlamentar',
                                 y = 'Vlr_Liquido')
# Alterando a cor de todas as barras para uma cor específica (ex: 'blue')
fig_gastos_partido_dep.update_traces(marker_color='gray')
                                

# Gasto total por partido no periodo
df_despesas_por_partido = df_despesas_filtered_3.groupby(['Partido']).agg({'Vlr_Liquido': 'sum'}).reset_index()

fig_total_gasto_partido = px.scatter(df_despesas_por_partido, x="Vlr_Liquido", size="Vlr_Liquido", color="Partido",
                                    log_x=True, size_max=65, text='Partido')

# Ajustando a posição do texto para aparecer dentro das bolas
fig_total_gasto_partido.update_traces(textposition='middle center')

# Removendo a legenda
fig_total_gasto_partido.update_layout(showlegend=False)

#-----------------------------------------------------------------------------------------------------------------#
# KPI´s - Calculos adcionais (cards)

qtde_partido = df_despesas_filtered['Partido'].nunique(), 
qtde_deputados = df_despesas_filtered['Nome_Parlamentar'].nunique()
total_gasto = round(df_despesas_filtered['Vlr_Liquido'].sum(),2)

media_gasto_geral = round(df_despesas_filtered_2['Vlr_Liquido'].describe(),2)
resumo = pd.DataFrame(media_gasto_geral)

# Função para formatar números no padrão brasileiro
def format_float_brasil(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Aplicando a função de formatação ao DataFrame
resumo_formatado = resumo.applymap(format_float_brasil)


#-----------------------------------------------------------------------------------------------------------------#
# Main

header = st.container()

with header:
    st.image('Logo/logo.png', width=250)
    st.title('Bem vindo ao projeto Câmara dos Deputados')
    st.text('Este projeto tem por finalidade acompanhar as despesas geradas por cada partido e deputado através da cota parlamentar')

st.divider()

st.markdown(f'### Dados coletados entre os anos de **{ano_menor}** a **{ano_maior}**!')
st.empty()

# Filtra o DataFrame pelo deputado selecionado
foto_parlamentar = df_despesas_filtered[df_despesas_filtered['Nome_Parlamentar'] == deputado_selecionado]
profissao_parlamentar = df_despesas_filtered[df_despesas_filtered['Nome_Parlamentar'] == deputado_selecionado]

col1, col2, col3 = st.columns(3)

with col1:
    if not foto_parlamentar.empty: # Verifica se o DataFrame filtrado não está vazio
        foto_parlamentar = foto_parlamentar.iloc[0]  # Acessa a primeira linha
        st.image(foto_parlamentar['URI_Deputado_Foto'], width=150)  # Exibe a foto
        st.subheader(f"Deputado: {(foto_parlamentar['Nome_Parlamentar'])} | Partido: {(foto_parlamentar['Partido'])}") # Exibe o nome
        st.subheader(f"Profissão: {(foto_parlamentar['Profissao'])}")
    else:
        st.write("Todos os parlamentares selecionados.")

with col2:
    st.metric("Quantidade de Deputados", qtde_deputados)
    st.metric("Quantidade de Partidos", qtde_partido[0])

with col3:
    st.subheader('Valor total gasto')
    st.metric('', format_currency(total_gasto, 'BRL', locale='pt_BR'))
    st.subheader('Resumo estatístico do Partido')
    st.data_editor(resumo_formatado, use_container_width=True)

st.divider()

div1, div2 = st.columns(2)
    
with div1:
    st.subheader(f'Gasto do(s) deputado(s) no ano de {ano_selecionado}')
    st.plotly_chart(fig_gastos_deput, use_container_width=True)

with div2:
    st.subheader(f'Gasto detalhado por tipo de despesa no ano de {ano_selecionado}')
    st.plotly_chart(fig_gastos_tipo, use_container_width=True)

st.divider()

st.subheader(f'Gasto por partido no ano de {ano_selecionado} aberto por parlamentar')
st.plotly_chart(fig_gastos_partido_dep, use_container_width=True)

st.subheader(f'Gasto total do partido no ano de {ano_selecionado}')
st.plotly_chart(fig_total_gasto_partido, use_container_width=True)
