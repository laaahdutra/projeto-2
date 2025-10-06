import streamlit as st

st.title("Meu programa")
st.write("Alô mundo") 
st.write("Agora o Colab é passado, venha para o Streamlit")

nome = st.text_input("Digite o seu nome:")
if nome:
    st.write (nome.upper())
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Caminho da imagem (no mesmo diretório do arquivo .py)
img = mpimg.imread('imagem programação.jpg')
plt.imshow(img)
plt.axis('off')  # Oculta os eixos
plt.show()
