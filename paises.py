import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Países")
dataset = pd.read_csv("https://www.irdx.com.br/media/uploads/paises.csv")

st.dataframe(dataset)

fig = px.scatter_geo(dataset,
                     lat=dataset['latitude'],
                     lon=dataset['longitude'],
                     hover_name=dataset['nome'])
fig.update_layout(title= 'Coordenadas dos Países do Mapa', geo_scope= 'world')

st.plotly_chart(fig,  use_container_width=True, theme="sreamlit") 
