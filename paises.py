import pandas as pd
import streamlit as st

st.title("Países")
dataset = pd.read_csv("https://www.irdx.com.br/media/uploads/paises.csv")

st.dataframe(dataset)
