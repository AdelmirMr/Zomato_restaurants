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
    page_title= "Visão Cidades", layout="wide",
    page_icon='🌇'
)



st.header("🌇 Visão Cidades")


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


#FUNÇÕES GRÁFICOS
def top_ten_cities_more_restaurants(df1):
    # Função que gera Gráfico com o TOP 10 Cidades com mais restaurantes na base de dados
    df_aux = (df1.loc[:, ['restaurant_id', 'city', 'country']]
              .groupby(['city', 'country'])
              .nunique()
              .sort_values('restaurant_id', ascending=False)
              .reset_index().head(10)
              )

    fig = (px.bar(df_aux, x='city', y='restaurant_id', text_auto=True, color='country',
                title="Top 10 Cidades com mais Restaurantes na Base de Dados",
                labels={
                 "city": "Cidades",
                 "restaurant_id": "Qtd Restaurantes",
                 "country": "paises"
                }))

    fig.update_layout(title_x=0.2)
    fig.update_layout(title_font_color='white')
    fig.update_traces(textfont_size=13, textangle=1, textposition="inside", cliponaxis=False)

    return fig

def top_seven_better_notes_city(df1):
    # Top 7 cidades com Restaurantes com média de avaliações acima de nota 4
    filtro = df1['aggregate_rating'] > 4
    df_aux = (df1.loc[filtro, ['restaurant_id', 'city', 'country']]
              .groupby(['city', 'country'])
              .count()
              .sort_values('restaurant_id', ascending=False)
              .reset_index().head(7))

    fig = px.bar(df_aux, x='city', y='restaurant_id', text_auto=True, color="country",
                 title="Top 7 Cidades com mais Restaurantes com nota acima de 4",
                 labels={
                     'restaurant_id': 'QTD de Restaurantes',
                     'city': 'Cidades',
                     'country': 'Países'
                 })
    fig.update_layout(title_x=0.2)
    fig.update_layout(title_font_color='white')
    fig.update_traces(textfont_size=13, textangle=1, textposition="inside", cliponaxis=False)

    return fig

def top_seven_bad_notes(df1):
        # Esta função plota um gráfico de barras com o top 7 Cidades com mais reataurantes com notas abaixo de 2,5
        filtro = df1['aggregate_rating'] < 2.5

        df_aux = (df1.loc[filtro, ['city', 'country', 'restaurant_id']]
                  .groupby(['city', 'country'])
                  .count()
                  .sort_values('restaurant_id', ascending=False)
                  .reset_index().head(7))

        fig = (px.bar(df_aux, x='city', y='restaurant_id',
                      title='Top 7 Cidades com Restaurantes com média de avaliações abaixo de 2,5',
                      text_auto=True, color='country',
                      labels={
                          'city': 'Cidades',
                          'restaurant_id': 'Restaurantes',
                          'country': 'Países'}))
        fig.update_layout(title_x=0.2)
        fig.update_layout(title_font_color='white')
        fig.update_traces(textfont_size=13, textangle=1, textposition="inside", cliponaxis=False)

        return fig


def top_ten_city_cuisines(df1):
    # Esta função plota um gráfico de barras com o top 10 cidades com mais tipos de culinárias únicas
    df_aux = (df1.loc[:, ['cuisines', 'city', 'country']]
              .groupby(['city', 'country'])
              .nunique()
              .sort_values('cuisines', ascending=False)
              .reset_index().head(10))

    fig = px.bar(df_aux, x='city', y='cuisines', color='country',
                 title="Top 10 Cidades com Restaurantes com tipos culinárias únicas", text_auto='True',
                 labels={
                     'city': 'Cidades',
                     'country': 'Países',
                     'restaurat_id': 'Restaurantes'
                 })
    fig.update_layout(title_x=0.2)
    fig.update_layout(title_font_color='white')
    fig.update_traces(textfont_size=13, textangle=1, textposition="inside", cliponaxis=False)

    return fig

#FUNÇÕES TRATAMENTO E LIMPEZA
def create_price_tye(price_range):
  if price_range == 1:
    return "cheap"
  elif price_range == 2:
    return "normal"
  elif price_range == 3:
    return "expensive"
  else:
    return "gourmet"

def rename_columns(dataframe):
    # Renomear as colunas do DataFrame
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
    default = ['Brazil','Canada', 'Qatar','South Africa','England', 'Australia'])

linhas_selecionadas = df1['country'].isin(country_choices)
df1 = df1.loc[linhas_selecionadas, :]

st.sidebar.markdown("""___""")
st.sidebar.markdown("### Powered by AdelmirMr")

# ============================================================
# DASHBOARDS
# ============================================================


with st.container():
    # Função gera um gráfico de barras com o TOP 10 cidades com mais restaurantes cadastrados
    fig =  top_ten_cities_more_restaurants(df1)
    st.plotly_chart(fig,use_container_width=True)


with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # Esta função plota um gráfico de barras com o top 7 Cidades com mais reataurantes com notas acima de 4
        fig = top_seven_better_notes_city(df1)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Esta função plota um gráfico de barras com o top 7 Cidades com mais reataurantes com notas abaixo de 2,5
        fig = top_seven_bad_notes(df1)
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    # Esta função plota um gráfico de barras com o top 10 cidades com mais tipos de culinárias únicas
    fig = top_ten_city_cuisines(df1)
    st.plotly_chart(fig, use_container_width=True)

