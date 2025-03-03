# bibliotecas
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import streamlit as st
from PIL import Image

st.set_page_config(
    layout="wide",
    page_title='Home',
    page_icon='📊'
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
    
    # Convertendo valores para Real BRL
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

#===============================================================================================================================================
# Barra Lateral
#===============================================================================================================================================

image_path = 'logo.png'
image = Image.open(image_path)

col1, col2 = st.sidebar.columns(2, gap='small')
with col1:
    st.image(image, width=40)
with col2:
    st.header('Fome Zero')

st.sidebar.markdown('##### Filtros')
country_select = st.sidebar.multiselect('Escolha os países que deseja visualizar os restaurantes', 
                                        df1['Country'].unique(),
                                        default = ['Brazil','England', 'Qatar', 'South Africa', 'Canada', 'Australia']
                                        )
                                         
df1 = df1[df1['Country'].isin(country_select)]

@st.cache_data
def convert_df(df1):

    return df1.to_csv().encode("utf-8")

csv = convert_df(df1)

st.sidebar.markdown('##### Dados Tratados')
st.sidebar.download_button(label= ('Download'),
                          data=csv,
                          file_name='clean_data.csv')
#===============================================================================================================================================
# Layout
#==============================================================================================================================================

with st.container():
    st.title('Fome Zero!')
    st.markdown('#### O melhor lugar para encontrar seu mais novo restaurante favorito!')
    st.markdown('##### Temos as seguintes marcas dentro da nossa plataforma:')

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric('Restaurantes cadastrados', 6929, help='Restaurantes cadastrados: 6929')
    col2.metric('Países cadastrados', 15, help='Países cadastrados: 15')
    col3.metric('Cidades cadastradas', 125, help='Cidades cadastradas: 125' )
    col4.metric('Avaliações feitas na plataforma', '4.638.535', help ='Avaliações feitas na plataforma: 4.638.535')
    col5.metric('Tipos de culinárias oferecidas', 165, help='Tipos de culinárias oferecidas: 165')

with st.container():
    f = folium.Figure(width=1920, height=1080)
    mapa = folium.Map(max_bounds=False, zoom_start=2).add_to(f)
    marker_cluster = MarkerCluster().add_to(mapa)

    for _, row in df1.iterrows():
        popup_text = f"""
        🍽️ Culinária: {row['Cuisines']}<br>
        💰 Preço médio para dois: R$ {row['Average_Cost_for_two']:.2f}<br>
        ⭐ Avaliação média: {row['Aggregate_rating']}
        """
    
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=row['Restaurant_Name'],
            popup=folium.Popup(popup_text, max_width=300),
        ).add_to(marker_cluster)

    st_folium( mapa, width=1024, height=768 )