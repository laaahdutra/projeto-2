import streamlit as st

st.title("Meu programa")
st.write("Alô mundo") 
st.write("Agora o Colab é passado, venha para o Streamlit")

nome = st.text_input("Digite o seu nome:")
if nome:
    st.write (nome.upper())
    st.image("imagens/programacao.jpg",
         caption="Eu na aula de hoje",
         use_container_width=True)
    
