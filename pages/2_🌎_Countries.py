# Libraries
from haversine import haversine
import plotly.express as px
import inflection
#import plotly.graph_objetcs as go

# Bibliotecas necessárias


import pandas as pd
import streamlit as st
import numpy as np
import folium
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static
import plotly.graph_objects as go

st.set_page_config(
    page_title= "Visão Países", layout="wide",
    page_icon='📊'
)
st.header("🌎 Visão Países")


#DICIONÁRIOS E COLEÇÕES

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}


#funcoes
def create_price_tye(price_range):
  if price_range == 1:
    return "cheap"
  elif price_range == 2:
    return "normal"
  elif price_range == 3:
    return "expensive"
  else:
    return "gourmet"

def qdt_cidades(df1):
    cols = ['country', 'city']
    df_aux = (df1.loc[:, cols]
            .groupby(['country'])
            .nunique()
            .reset_index()
            .sort_values('city', ascending=False))

    #desenhando o gráfico de barras
    fig = px.bar(df_aux, x = "country", y = "city", text_auto=True, labels={
        "country" : "Países",
        "city" : "Cidades"
    })
     #Editanto os parâmetros do gráfico
    fig.update_layout(
        title=dict(text="Quantidade de Cidades Registradas por País", font=dict(size=15), automargin=True,
                yref='paper')
    )
    return fig

def qtd_restaurnt_country(df1):
    cols = ['country', 'restaurant_id']
    df_aux = (df1.loc[:, cols]
              .groupby(['country'])
              .count()
              .reset_index()
              .sort_values('restaurant_id', ascending=False)
              )
    # desenhando o gráfico de barras
    fig = px.bar(df_aux, x='country', y='restaurant_id', text_auto=True, labels={
        "country" : "Países",
        "restaurant_id" : "Restaurantes"
    })
    return fig


def votes_country(df1):
    df_aux = (df1.loc[:, ['country', 'votes']].groupby('country').mean().reset_index().sort_values('votes',
                                                                                                  ascending=False))

    fig = px.bar(df_aux, x='country', y='votes', text_auto=True, labels={
        "country": "Países",
        "votes": "Avaliações",
    })
    # Editanto os parâmetros do gráfico
    fig.update_layout(
        title=dict(text="Média de Avaliações feitas por País", font=dict(size=15), automargin=True,
                 yref='paper')
    )
    return fig


def price_for_two(df1):
    filtro = df1['average_cost_for_two'] == 1


    df_aux = df1.loc[:, ['average_cost_for_two', 'country']].groupby('country').mean().reset_index().sort_values(
        'average_cost_for_two', ascending=False)
    fig = px.bar(df_aux, x='country', y='average_cost_for_two', text_auto=True, labels={
        "average_cost_for_two" : "Média de preço",
        "country" : "Países"
    })
    # Editanto os parâmetros do gráfico
    fig.update_layout(
        title=dict(text="Média de Preço de um prato para duas pessoas por País", font=dict(size=15), automargin=True,
                yref='paper')
    )
    return fig
# Renomear as colunas do DataFrame
def rename_columns(dataframe):
    df1 = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df1

def color_name(color_code):
  return COLORS[color_code]

def clean_code(df1):
    df1 = df.copy()

    #removendo linhas duplicadas
    df1 = df1.drop_duplicates()
    df1 = rename_columns(df1)
    # dicionario com nome dos países
    df1['country_code'] = df1['country_code'].replace({
        1: "India",
        14: "Australia",
        30: "Brazil",
        37: "Canada",
        94: "Indonesia",
        148: "New Zeland",
        162: "Philippines",
        166: "Qatar",
        184: "Singapure",
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "United Arab Emirates",
        215: "England",
        216: "United States of America",
    })
    df1['rating_color'] = df1['rating_color'].replace({
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred",
    })
    # convertenta a coluna Causines para str
    df1['cuisines'] = df1['cuisines'].astype(str)
    # categorizando o restaurante apenas pela primeira cozinha que aparece na coluna
    df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])
    df1.rename({"country_code": "country"}, axis=1, inplace=True)

    return df1

df = pd.read_csv('dataset/zomato.csv')

#limpando dados
df1 = clean_code(df)




## ----------------------------------------------------
# MENU LATERAL
# ---------------------------------------------------

st.sidebar.image('zomato_logo2.png', width=300,  )

#st.sidebar.markdown("""______""")

st.sidebar.markdown('# Olá, seja bem vindo à Zomato Restaurants')
st.sidebar.markdown("""---""")


st.sidebar.markdown('#### Filtros')
country_choices = st.sidebar.multiselect(
    'Escolha os Paises que Deseja visualizar os Restaurantes?',
    ['India','Australia', 'Brazil', 'Canada', 'Indonesia','New Zeland','Philippines','Qatar',
     'Singapure', 'South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'],
    default = ['Australia','Qatar','England','South Africa', 'Brazil', 'Canada'])

linhas_selecionadas = df1['country'].isin(country_choices)
df1 = df1.loc[linhas_selecionadas, :]

st.sidebar.markdown("""___""")
st.sidebar.markdown("### Powered by AdelmirMr")


#==================================================
# CONTEÚDO
#==================================================

# Quantidade de Restaurantes registrados por pais
with st.container():

    fig = qtd_restaurnt_country(df1)
    fig.update_layout(
        title=dict(text="Quantidade de Restaurantes Registrados por País", font=dict(size=15), automargin=True,
                   yref='paper')
    )
    st.plotly_chart(fig, use_container_width=True)


# Quantidade de Cidades Registrados por País
with st.container():

    fig = qdt_cidades(df1)
    st.plotly_chart(fig, use_container_width=True)


with st.container():
    col1, col2 = st.columns(2)
    # Media de avaliações feitas por pais
    with col1:
        fig = votes_country(df1)
        st.plotly_chart(fig, use_container_width=True)

    # Valor médio de um prato pra duas pessoas por país
    with col2:

        fig = price_for_two(df1)
        st.plotly_chart(fig, use_container_width=True)