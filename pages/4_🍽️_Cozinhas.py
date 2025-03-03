# bibliotecas
import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from PIL import Image

st.set_page_config(
    layout="wide",
    page_title='Cozinhas',
    page_icon='🍽️'
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

#=================================================================================================================================================
# Barra Lateral
#=================================================================================================================================================

st.sidebar.markdown('## Filtros')
country_select = st.sidebar.multiselect('Escolha os países que deseja visualizar as informações', 
                                        df1['Country'].unique(),
                                        default = ['Brazil','England', 'Qatar', 'South Africa', 'Canada', 'Australia']
                                        )


#df1 = df1[df1['Country'].isin(country_select)]

count_restaurant_select = st.sidebar.slider('Selecione a quantidade de restaurantes que deseja visualizar', 1, 20, value=10)
cuisine_select = st.sidebar.multiselect('Escolha os tipos de culinária', 
                                        df1['Cuisines'].unique(),
                                        default = ['Brazilian', 'Japanese','Italian', 'French', 'Pizza']
                                        )

#df1 = df1[df1['Cuisines'].isin(cuisine_select)]


if not country_select:
    country_select = df1['Country'].unique()  # Exibe todos os países se não houver filtro
if not cuisine_select:
    cuisine_select = df1['Cuisines'].unique()  # Exibe todos os tipos de culinária se não houver filtro

# Aplicando os filtros no dataframe
df1 = df1[df1['Country'].isin(country_select) & df1['Cuisines'].isin(cuisine_select)]



#================================================================
# Layout no Streamlit
#================================================================

st.header('🍽️ Visão Cozinhas')
st.markdown('''___''')
st.subheader('Melhores restaurantes dos principais tipos culinários')

cols = ['Cuisines', 'Aggregate_rating','Restaurant_Name']
df_aux = df1.loc[:, cols].groupby(['Cuisines','Restaurant_Name']).mean().round(2).sort_values('Aggregate_rating', ascending = False).reset_index()
df_aux = df_aux.iloc[0:5]


col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('North Indian: Indian Grill Room', '4.9/5.0', help='Restaurante: Indian Grill Room' f'\n\nPaís: India'f'\n\nCidade: Gurgaon' f'\n\nMédia prato pra 2: R$108.0')
col2.metric('North Indian: Pirates of Grill	', '4.9/5.0', help='Restaurante: Pirates of Grill' f'\n\nPaís: India'f'\n\nCidade: Gurgaon' f'\n\nMédia prato pra 2: R$120.0')
col3.metric('Italian: Darshan', '4.9/5.0', help='Restaurante: Darshan' f'\n\nPaís: India' f'\n\nCidade: Pune' f'\n\nMédia prato pra 2: R$42.0')
col4.metric('North Indian: Barbeque Nation', '4.9/5.0', help='Restaurante: Barbeque Nation' f'\n\nPaís: India'f'\n\nCidade: Kolkata' f'\n\nMédia prato pra 2: R$108.0')
col5.metric("European: AB's - Absolute Barbecues", '4.9/5.0', help="Restaurante: AB's - Absolute Barbecues" f'\n\nPaís: India'f'\n\nCidade: Bangalore' f'\n\nMédia prato pra 2: R$96.0')

       
with st.container():
    st.subheader(f'Top {count_restaurant_select} Restaurantes')
    cols = ['Restaurant_ID', 'Restaurant_Name','Country', 'City', 'Cuisines','Average_Cost_for_two', 'Aggregate_rating', 'Votes']
    df_aux = df1.loc[:, cols].groupby(['Restaurant_ID','Restaurant_Name','Country','City','Cuisines']).agg({'Average_Cost_for_two':'mean', 'Aggregate_rating': 'mean', 'Votes': 'sum'}).sort_values(['Aggregate_rating', 'Restaurant_ID'], ascending = [False, True]).reset_index()
    df_aux = df_aux.iloc[0:count_restaurant_select]
    st.dataframe(df_aux)
    st.markdown('''___''')

with st.container():
    col1, col2 = st.columns(2, gap='large')
    with col1:
        cols = ['Cuisines', 'Aggregate_rating']
        df_aux = df1.loc[:, cols].groupby('Cuisines').mean().sort_values('Aggregate_rating', ascending = False).round(2).reset_index()
        df_aux = df_aux.iloc[0:count_restaurant_select]
        fig = px.bar(df_aux, x='Cuisines', y='Aggregate_rating', title=f'Top {count_restaurant_select} melhores tipos de culinárias', color='Cuisines', text='Aggregate_rating', labels={'Cuisines': 'Tipos de culinária','Aggregate_rating': 'Média da avaliação média'} )
        st.plotly_chart(fig)

    with col2:
        cols = ['Cuisines', 'Aggregate_rating']
        df_aux = df1.loc[:, cols].groupby('Cuisines').mean().sort_values('Aggregate_rating', ascending = True).round(2).reset_index()
        df_aux = df_aux.iloc[0:count_restaurant_select]
        fig = px.bar(df_aux, x='Cuisines', y='Aggregate_rating', title=f'Top {count_restaurant_select} piores tipos de culinárias', color='Cuisines', text='Aggregate_rating', labels={'Cuisines': 'Tipos de culinária','Aggregate_rating': 'Média da avaliação média'} )
        st.plotly_chart(fig)
