import streamlit as st

st.title("Meu programa")
st.write("Alô mundo") 
st.write("Agora o Colab é passado, venha para o Streamlit")

st.text_imput("Digite o seu nome:")
if nome:
    st.write(nome.upper())
