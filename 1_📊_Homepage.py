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
    page_title= "Visão Geral", layout="wide",
    page_icon='📊'
)

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

# Renomear as colunas do DataFrame tirar, remover espaço em branco e adicionar undersore entre palavras do titulo
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
def general_metrics():
    #restaurantes unicos cadastrados

        with col1:
            u_restaurants = len(df1.loc[:, 'restaurant_name'].unique())
            col1.metric('Restaurantes Cadastrados', u_restaurants)

        # Países Cadastrados
        with col2:
            u_country = len(df1.loc[:, 'country'].unique())
            col2.metric('Países Cadastrados', u_country)

        # Cidades Cadastradas
        with col3:
            u_cities = len(df1.loc[:, 'city'].unique())
            col3.metric('Cidades Cadastradas', u_cities)

        # Avaliações Feitas na Plataforma
        with col4:
            votos = df1.loc[:, 'votes'].sum()
            resultado = '{0:,}'.format(votos).replace(',', '.')
            col4.metric('Qtd Avaliações Feitas', resultado)

        # Tipos de Culinárias Oferecidas
        with col5:
            types_cuisines = len(df1.loc[:, 'cuisines'].unique())
            col5.metric('tipos de Culinárias Oferecidas', types_cuisines)


def location_graph():
    # Apresentar a localidade de onde estão situados os restaurantes

    # Cria o painel no qual o mapa será adicionado
    fig = folium.Figure(width=1080, height=720)
    # Cria o objeto map e adiciona ao painel
    m = folium.Map(max_bounds=True, zoom_start=1000).add_to(fig)

    # A função 'MarkerCluster()' cria um objeto que agrupará
    # os marcadores dependendo do zoom aplicado ao mapa. No comando
    # abaixo estamos criando um objeto do tipo 'MarkerCluster'
    # (instanciando a classe) e o adicionando ao mapa
    marker_cluster = MarkerCluster().add_to(m)

    # O método '.iterrows()' do objeto dataframe cria um iterador cujo os elementos
    # são tuplas contendo dois elemento: o indice da linha e o conteúdo da linha (series)

    for _, line in df1.iterrows():
        folium.Marker(
            location=(line['latitude'], line['longitude']),
            popup=('Culinária: ' + line['cuisines']),
            tooltip=(line['restaurant_name']),
            icon=folium.Icon(color=line['rating_color'], icon='pushpin'),

        ).add_to(marker_cluster)

    folium_static(m, width=1080, height=720)
df = pd.read_csv('dataset/zomato.csv')

#limpando dados
df1 = clean_code(df)

# ===============================
# Barra lateral Filtros
# ==============================

st.header('Fome Zero')
st.markdown('#### O melhor lugar para encontrar seu mais novo restaurante favorito!')
st.markdown('##### Temos as seguintes marcas dentro da nossa plataforma:')


## ----------------------------------------------------
# MENU LATERAL
# ---------------------------------------------------

#st.sidebar.markdown("""______""")

st.sidebar.image('zomato_logo2.png', width=300,  )

#st.sidebar.markdown("""______""")

st.sidebar.markdown('# Olá, seja bem vindo à Zomato Restaurants')
st.sidebar.markdown("""---""")


st.sidebar.markdown('#### Filtros')
country_choices = st.sidebar.multiselect(
    'Escolha os Paises que Deseja visualizar os Restaurantes?',
    ['India','Australia', 'Brazil', 'Canada', 'Indonesia','New Zeland','Philippines','Qatar',
     'Singapure', 'South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'],
    default = ['India','Australia', 'Brazil', 'Canada'])

## Aplicando o filtro a todo o dataframe
linhas_selecionadas = df1['country'].isin(country_choices)
df1 = df1.loc[linhas_selecionadas, :]



st.sidebar.markdown("""___""")
st.sidebar.markdown("### Powered by AdelmirMr")

# Filtros de data


# ==========================================
# LAYOUT NO STREAMLIT
# ==========================================



# conteiner com os numeros geral

with st.container():
    st.subheader('Métricas Gerais')

    col1, col2, col3, col4, col5 = st.columns(5)
    # Função retornar as métricais gerais em uma linha
    # 1 -Restaurantes Cadastrados
    # 2 - Países Cadastrados
    # 3 - Cidades Cadastradas
    # 4 - Qtd Avaliações Feitas
    # 5 - Ipos de Culináiras oferecidas
    general_metrics()

with st.container():
    ## Apresentar a localidade de onde estão situados os restaurantes
    location_graph()







