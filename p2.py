import streamlit as st
import requests

# Função para consultar jurisprudência na API do DataJud
def consultar_jurisprudencia(tema):
    url = "https://api.datajud.jus.br/jurisprudencia"
    params = {"q": tema, "limit": 5}  # Limita a 5 resultados
    response = requests.get(url, params=params)
    return response.json()

# Interface do Streamlit
st.title("Consulta de Jurisprudência")
tema = st.text_input("Digite o tema da pesquisa")

if st.button("Buscar"):
    if tema:
        resultados = consultar_jurisprudencia(tema)
        if resultados:
            st.write(f"**Resultados para: {tema}**")
            for item in resultados.get("data", []):
                st.subheader(item["titulo"])
                st.write(f"**Relator:** {item['relator']}")
                st.write(f"**Data de Julgamento:** {item['data_julgamento']}")
                st.write(f"**Resumo:** {item['resumo']}")
                st.write(f"[Leia mais]({item['url']})")
        else:
            st.warning("Nenhum resultado encontrado.")
    else:
        st.error("Por favor, insira um tema para a pesquisa.")
