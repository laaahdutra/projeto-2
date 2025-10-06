import streamlit as st

st.title("Meu programa")
st.write("Alô mundo") 
st.write("Agora o Colab é passado, venha para o Streamlit")

nome = st.text_input("Digite o seu nome:")
if nome:
    st.write (nome.upper())
st.image("programacaoo.jpg")
st.write("Eu na aula de hoje programando")
st.image("meninadandooiprog.jpg")
st.write("Oiii, Josir!! Bem vindo!")
