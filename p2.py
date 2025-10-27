# app.py
import streamlit as st
import requests

# Título da aplicação
st.title("Consulta de Deputados - Câmara dos Deputados")

# Campo para o usuário digitar o nome do deputado
nome_deputado = st.text_input("Digite o nome do deputado:")

if nome_deputado:
    # Chamada à API da Câmara dos Deputados
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados?nome={nome_deputado}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Verifica se encontrou algum deputado
        deputados = data.get("dados", [])
        
        if deputados:
            # Exibe as informações em formato de tabela
            st.subheader("Resultados da busca:")
            for deputado in deputados:
                st.write(f"**Nome:** {deputado.get('nome')}")
                st.write(f"**ID:** {deputado.get('id')}")
                st.write(f"**Sigla do Partido:** {deputado.get('siglaPartido')}")
                st.write(f"**UF:** {deputado.get('siglaUf')}")
                st.markdown("---")
        else:
            st.warning("Nenhum deputado encontrado com esse nome.")
            
    except requests.RequestException as e:
        st.error(f"Erro ao consultar a API: {e}")
