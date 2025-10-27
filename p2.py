import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# URL do arquivo GeoJSON dos estados brasileiros
geojson_url = "https://raw.githubusercontent.com/giuliano-macedo/geodata-br-states/main/geojson/br_states.json"

# Carregar dados da população carcerária
@st.cache_data
def carregar_dados():
    # Substitua pela URL do seu arquivo CSV no GitHub
    csv_url = "https://raw.githubusercontent.com/seu_usuario/seu_repositorio/main/populacao_carceraria.csv"
    df = pd.read_csv(csv_url)
    return df

# Carregar o GeoJSON
@st.cache_data
def carregar_geojson():
    response = requests.get(geojson_url)
    return response.json()

# Carregar os dados
df = carregar_dados()
geojson = carregar_geojson()

# Mesclar os dados da população carcerária com as informações geográficas
# Supondo que o CSV tenha as colunas 'sigla' e 'populacao_carceraria'
df_merged = df.merge(pd.DataFrame(geojson['features']), left_on='sigla', right_on='properties.sigla')

# Criar o mapa interativo
fig = px.choropleth(
    df_merged,
    geojson=geojson,
    locations='properties.sigla',
    color='populacao_carceraria',
    hover_name='properties.sigla',
    hover_data=['populacao_carceraria'],
    color_continuous_scale="Viridis",
    labels={'populacao_carceraria': 'População Carcerária'},
    title="População Carcerária por Estado"
)

# Atualizar layout do mapa
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Exibir o mapa
st.plotly_chart(fig)

# Exibir tabela de dados
if st.checkbox("Mostrar tabela de dados"):
    st.write(df)

