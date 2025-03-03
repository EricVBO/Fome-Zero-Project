# 📌 Fome Zero 

## 🎯 1. Problema de Negócio
A Fome Zero é uma plataforma de tecnologia que conecta restaurantes, entregadores e clientes com o objetivo de simplificar a busca por restaurantes e aprimorar a experiência dos usuários, fornecendo informações como:

1. Localização dos restaurantes
2. Preço dos pratos
3. Tipos de culinária oferecidos
4. Avaliações e feedbacks dos clientes

O CEO deseja tomar decisões estratégicas para expandir a atuação da Fome Zero e melhorar a experiência dos usuários. Para isso, preciso responder perguntas-chave sobre o mercado e a operação da empresa.

## 📌 2. Premissas Assumidas para a Análise
Todos os dados foram extraídos da plataforma Kaggle no link: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv

Os valores monetários foram convertidos para Real Brasileiro (BRL) utilizando taxas de câmbio aproximadas.

Marketplace foi o modelo de negócio assumido.

As 3 principais visões do negócio foram: Visão Países, Visão Cidades, Visão Cozinhas.

## 🚀 3. Estratégia da Solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as principais visões do modelo de negócio da empresa, a partir de três perspectivas:
### 🌍 Visão Países
    1. Em quais países a Fome Zero tem maior presença?
    2. Qual o ticket médio dos restaurantes por país?
    3. Qual a distribuição de avaliações por país?
### 🏙️ Visão Cidades
    1. Quais cidades possuem mais restaurantes cadastrados?
    2. Como a avaliação dos restaurantes varia entre as cidades?
    3. Quais cidades possuem mais tipos de culinárias?
### 🍽️ Visão Cozinhas
    1. Quais são os restaurantes mais bem avaliados?
    2. Como a avaliação dos tipos de culinárias variam entre elas?

## 📊 4. Top 3 Insights de Dados
    🔹 O país com mais restaurantes cadastrados é a Índia, seguida por Estados Unidos e Inglaterra.
    🔹 Indonésia apesar de apenas 3 cidades cadastradas, possui maior número de avaliações no geral.
    🔹 Birmingham, na Inglaterra, é a cidade com maior variedade de culinárias.

## 📌 5. O Produto Final do Projeto
O resultado do projeto foi um dashboard interativo desenvolvido com Streamlit, onde é possível visualizar as análises realizadas a partir de diferentes filtros. As principais funcionalidades incluem:
1. Mapa interativo com a localização dos restaurantes
2. Gráficos dinâmicos para comparação entre países, cidades e tipos de culinária
3. Tabelas exploratórias para análise detalhada dos dados

📌 Link do Dashboard: https://ericvbo-project-fome-zero.streamlit.app

## 📌 6. Conclusão
O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam as métricas de forma clara e objetiva para o CEO.

Com base nos insights gerados, o CEO pode tomar decisões mais embasadas para expandir os negócios da Fome Zero, focando nos países com mais restaurantes cadastrados e criando estratégias para impulsionar países com menor demanda, nas cidades mais estratégicas e nos tipos de culinária mais bem avaliados. Além disso, a empresa pode incentivar melhorias na experiência dos clientes ao compreender a relação entre preço e avaliações dos restaurantes.

## 📌 7. Próximos Passos
    🔹 Expandir a análise para considerar mais hipóteses, por exemplo, a relação do valor do prato com a renda per capita do local.
    🔹 Utilizar API de conversão monetária, para visualização dos valores de acordo com a moeda de cada país.
    🔹 Criar novos filtros.
    🔹 Automatizar a coleta de dados para manter as informações sempre atualizadas.

#### 📌 Tecnologias Utilizadas: Python, Pandas, Plotly, Streamlit, Folium
#### 📌 Contato: ericvbo@outlook.com
