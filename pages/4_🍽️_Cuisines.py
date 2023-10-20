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
    page_title= "Visão Cozinhas", layout="wide",
    page_icon='🍽️'
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
def top_better_restaurant(df1):
    filter = df1['aggregate_rating'] >= 4.9
    df_aux = (df1.loc[
                  filter, ['restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines', 'average_cost_for_two',
                           'aggregate_rating', 'votes']].
              groupby(['restaurant_name'])
              .max(['aggregate_rating', 'votes'])
              .sort_values('votes', ascending=False).reset_index()
              )

    df_aux1 = df_aux.head(qtd_restaurant)
    return df_aux1


def top_better_cuisines(df1):
    filter = df1['aggregate_rating'] >= 4.0
    df2 = (df1.loc[filter, ['cuisines', 'aggregate_rating']]
           .groupby(['cuisines'])
           .max()
           .sort_values('aggregate_rating', ascending=False)
           .reset_index()
           )
    df2 = df2.head(qtd_restaurant)
    fig = px.bar(df2, x='cuisines', y='aggregate_rating', text_auto=True,
                 labels={'aggregate_rating': 'Avaliação Média', 'cuisines': 'Culinária'})
    return fig


def top_worst_cuisines(df1):
    filter = df1['aggregate_rating'] <= 2.5
    df2 = (df1.loc[filter, ['cuisines', 'aggregate_rating']]
           .groupby(['cuisines'])
           .max()
           .sort_values('aggregate_rating', ascending=False).reset_index()
           )
    df2 = df2.head(qtd_restaurant)
    fig = px.bar(df2, x='cuisines', y='aggregate_rating', text_auto=True,
                 labels={'aggregate_rating': 'Avaliação Média', 'cuisines': 'Culinária'})
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




## -======================================================
#                       MENU LATERAL
# =======================================================
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

qtd_restaurant = st.sidebar.slider('Selecione a quantidade de Restaurantes que deseja visualizar:', 1, 20, 10)

default_options = ['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian', 'Others', 'Tex-Mex', 'Vegetarian', 'Durban', 'Beverages', 'Coffee', 'Pizza', 'Chinese', 'European', 'Seafood', 'Fresh Fish', 'Fish and Chips', 'Street Food' ]
cuisine_choices = st.sidebar.multiselect('Escolha os Tipos de Culinária:',
                                           df1['cuisines'].unique(), default=default_options)

#Filtro de países
linhas_selecionadas = df1['country'].isin(country_choices)
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de culinárias
linhas_selecionadas = df1['cuisines'].isin(cuisine_choices)
df1 = df1.loc[linhas_selecionadas, :]


st.sidebar.markdown("""___""")
st.sidebar.markdown("### Powered by AdelmirMr")


# ============================================================
# DASHBOARDS
# ============================================================
st.title("🍽️ Visão Tipos de Cozinhas")
st.markdown('## Melhores Restaurantes dos Principais tipos de Culinárias')

col1, col2, col3, col4, col5 = st.columns(5)

with st.container():

    # Função retornar as métricais gerais em uma linha
    # 1 - Melhor culinária
    # 2 - Nota Melhor Culinária
    # 3 - Pior culinária
    # 4 - Nota Pior culinária

    cols = ['aggregate_rating', 'restaurant_id', 'restaurant_name', 'average_cost_for_two', 'currency', 'votes',
            'country', 'city']

    best_JP = (df1[df1.cuisines == 'Japanese'][cols]
               .sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True])
               .head(1).reset_index(drop=True))

    best_BR = (df1[df1.cuisines == 'Brazilian'][cols]
               .sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True])
               .head(1).reset_index(drop=True))

    best_IT = (df1[df1.cuisines == 'Italian'][cols]
               .sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True])
               .head(1).reset_index(drop=True))

    best_CH = (df1[df1.cuisines == 'Chinese'][cols]
               .sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True])
               .head(1).reset_index(drop=True))

    best_AB = (df1[df1.cuisines == 'Arabian'][cols]
               .sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True])
               .head(1).reset_index(drop=True))
    col1, col2, col3, col4, col5 = st.columns(5)



    with col1:
       # Japonesa
         st.metric(label=f'Japonesa: {best_JP.restaurant_name[0]}',
                  value=f'{best_JP.aggregate_rating[0]}/5.0',
                    help=f"""
                        País: {best_JP.country[0]} \n
                        Cidade: {best_JP.city[0]} \n
                        Preço para duas pessoas: {best_JP.currency[0]}{best_JP.average_cost_for_two[0]} 
                        """
                 )
    with col2:
        # Brasileira
        st.metric(label=f'Brasileira: {best_BR.restaurant_name[0]}',
                  value=f'{best_BR.aggregate_rating[0]}/5.0',
                  help=f"""
               País: {best_BR.country[0]} \n
               Cidade: {best_BR.city[0]} \n
               Preço para duas pessoas: {best_BR.currency[0]}{best_BR.average_cost_for_two[0]} 
               """
                  )
    with col3:
        # Italiana
        st.metric(label=f'Italiana: {best_IT.restaurant_name[0]}',
                  value=f'{best_IT.aggregate_rating[0]}/5.0',
                  help=f"""
                País: {best_IT.country[0]} \n
                Cidade: {best_IT.city[0]} \n
                Preço para duas pessoas: {best_IT.currency[0]}{best_IT.average_cost_for_two[0]} 
                """
                  )
    with col4:
        # Chinesa
        st.metric(label=f'Chinesa: {best_CH.restaurant_name[0]}',
                  value=f'{best_CH.aggregate_rating[0]}/5.0',
                  help=f"""
                        País: {best_CH.country[0]} \n
                        Cidade: {best_CH.city[0]} \n
                        Preço para duas pessoas: {best_CH.currency[0]}{best_CH.average_cost_for_two[0]} 
                        """
                  )
    with col5:
        # Árabe
        st.metric(label=f'Árabe: {best_AB.restaurant_name[0]}',
                  value=f'{best_AB.aggregate_rating[0]}/5.0',
                  help=f"""
                   País: {best_AB.country[0]} \n
                   Cidade: {best_AB.city[0]} \n
                   Preço para duas pessoas: {best_AB.currency[0]}{best_AB.average_cost_for_two[0]} 
                   """
                  )




with st.container():
# Top x restaurantes

    df_aux = top_better_restaurant(df1)
    df_aux1 = df_aux.head(qtd_restaurant)
    st.markdown(f'#### Top {qtd_restaurant} Restaurantes')
    st.dataframe(df_aux1, use_container_width=True)


with st.container():
    col1, col2 = st.columns(2)

    # Top x melhores culinárias
    with col1:

        fig = top_better_cuisines(df1)
        st.markdown(f'#### Top {qtd_restaurant} Melhores Culinárias:')
        st.plotly_chart(fig, use_container_width=True)

    # Top x piores culinárias
    with col2:
        fig  = top_worst_cuisines(df1)
        st.markdown(f'#### Top {qtd_restaurant} Piores Culinárias:')
        st.plotly_chart(fig, use_container_width=True)
