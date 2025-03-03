# bibliotecas
import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from PIL import Image

st.set_page_config(
    layout="wide",
    page_title='Cidades',
    page_icon='🏙️'
)

#-------------------------------------------------------------------------------------------------------------------------------------------------

def clean_df(df1):
    # substituição dos espaços vazios dos nomes das colunas por _
    df1.columns = df1.columns.str.replace(" ", "_")
    
    # função para atribuir os nomes dos países ao Country_Code
    COUNTRIES = {
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
    }
    
    def country_name(Country_Code):
        
        return COUNTRIES[Country_Code]
        
    # Criando coluna 'Country' e aplicando a função
    df1['Country'] = df1['Country_Code'].apply(country_name)

    def create_price_tye(price_range):
        if price_range == 1:
            return "cheap"
        elif price_range == 2:
            return "normal"
        elif price_range == 3:
            return "expensive"
        else:
            return "gourmet"
    
    df1['Price_range'] = df1['Price_range'].apply(create_price_tye)
    
    # Taxas de câmbio aproximadas (1 unidade da moeda local para BRL)
    exchange_rates = {
        "Philippines": 0.09,   # 1 PHP ≈ 0.09 BRL
        "Brazil": 1.00,        # Já está em BRL
        "Australia": 3.30,     # 1 AUD ≈ 3.30 BRL
        "United States of America": 4.90,  # 1 USD ≈ 4.90 BRL
        "Canada": 3.65,        # 1 CAD ≈ 3.65 BRL
        "Singapure": 3.65,     # 1 SGD ≈ 3.65 BRL
        "United Arab Emirates": 1.33,  # 1 AED ≈ 1.33 BRL
        "India": 0.060,        # 1 INR ≈ 0.060 BRL
        "Indonesia": 0.00032,  # 1 IDR ≈ 0.00032 BRL
        "New Zeland": 3.00,    # 1 NZD ≈ 3.00 BRL
        "England": 6.30,       # 1 GBP ≈ 6.30 BRL
        "Qatar": 1.34,         # 1 QAR ≈ 1.34 BRL
        "South Africa": 0.26,  # 1 ZAR ≈ 0.26 BRL
        "Sri Lanka": 0.016,    # 1 LKR ≈ 0.016 BRL
        "Turkey": 0.16,        # 1 TRY ≈ 0.16 BRL
    }

    df1['Average_Cost_for_two'] = df1.apply(lambda row: row['Average_Cost_for_two'] * exchange_rates.get(row['Country'], 1), axis=1)
        
    # Excluindo valores NaN da coluna Cuisines
    df1 = df1.dropna(subset=['Cuisines'])
    
    # Excluindo linha com valor outlier
    df1 = df1.drop(index=385)
    
    # Função para splitar a coluna Cuisines e pegar o 1º dado antes da vírgula
    df1['Cuisines'] = df1.loc[:, 'Cuisines'].apply(lambda x: x.split(',')[0])

    return df1
    
# leitura e armazenamento do arquivo csv
df = pd.read_csv('dataset/zomato.csv')

df1 = clean_df( df )

#================================================================================================================================================
# Barra Lateral
#================================================================================================================================================

st.sidebar.markdown('## Filtros')
country_select = st.sidebar.multiselect('Escolha os países que deseja visualizar as informações', 
                                        df1['Country'].unique(),
                                        default = ['Brazil','England', 'Qatar', 'South Africa', 'Canada', 'Australia']
                                        )
                                         
df1 = df1[df1['Country'].isin(country_select)]

#================================================================================================================================================
# Layout no Streamlit
#================================================================================================================================================
st.header('🏙️ Visão Cidades')
st.markdown('''___''')

with st.container():  
    cols = ['City', 'Restaurant_ID', 'Country' ]
    df_aux = df1.loc[:, cols].groupby(['City','Country']).count().sort_values('Restaurant_ID', ascending = False).reset_index()
    df_aux = df_aux.iloc[0:10]
    fig = px.bar(df_aux, x='City', y='Restaurant_ID', color= 'Country', text='Restaurant_ID', title='Top 10 cidades com mais restaurantes cadastrados', labels={'City':'Cidades', 'Restaurant_ID': 'Quantidade de restaurantes', 'Country': 'Países'})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('''___''')

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        cols = ['City','Country','Restaurant_ID']
        df_aux = df1.loc[df1['Aggregate_rating'] > 4 ]
        df_aux = df_aux.loc[:, cols].groupby(['City', 'Country']).count().sort_values('Restaurant_ID', ascending = False).reset_index()
        df_aux = df_aux.iloc[0:10]
        fig = px.bar(df_aux, x='City', y='Restaurant_ID', color='Country', text='Restaurant_ID', title='Top 10 cidades com restaurantes com média de avaliação acima de 4', labels={'City':'Cidades', 'Restaurant_ID': 'Quantidade de restaurantes', 'Country': 'Países'})
        st.plotly_chart(fig, use_container_width=True)   
    with col2:
        cols = ['City','Country','Restaurant_ID']
        df_aux = df1.loc[df1['Aggregate_rating'] < 2.5 ]
        df_aux = df_aux.loc[:, cols].groupby(['City', 'Country']).count().sort_values('Restaurant_ID', ascending = False).reset_index()
        df_aux = df_aux.iloc[0:10]
        fig = px.bar(df_aux, x='City', y='Restaurant_ID', color='Country', text='Restaurant_ID', title='Top 10 cidades com restaurantes com média de avaliação abaixo de 2.5', labels={'City':'Cidades', 'Restaurant_ID': 'Quantidade de restaurantes', 'Country': 'Países'})
        st.plotly_chart(fig, use_container_width=True)
st.markdown('''___''')

with st.container():
    cols = ['City', 'Cuisines', 'Country']
    df_aux = df1.loc[:, cols].groupby(['City', 'Country']).nunique().sort_values('Cuisines', ascending = False).reset_index()
    df_aux = df_aux.iloc[:10]
    fig = px.bar(df_aux, x='City', y='Cuisines', color='Country', text='Cuisines', title='Top 10 cidades com mais restaurantes com tipos culinários distintos', labels={'City':'Cidades','Cuisines':'Quantidade de tipos culinários únicos', 'Country':'Países'})
    st.plotly_chart(fig, use_container_width=True)