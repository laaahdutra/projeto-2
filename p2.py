# app.py
import streamlit as st
import requests
import pandas as pd

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
        
        deputados = data.get("dados", [])
        
        if deputados:
            # Criar lista de dicionários com informações
            lista_info = []
            for deputado in deputados:
                lista_info.append({
                    "Nome": deputado.get("nome"),
                    "ID": deputado.get("id"),
                    "Sigla Partido": deputado.get("siglaPartido"),
                    "UF": deputado.get("siglaUf"),
                    "URL Perfil": deputado.get("uri")
                })
            
            # Transformar em DataFrame e mostrar
            df = pd.DataFrame(lista_info)
            st.table(df)  # ou st.dataframe(df) para tabela interativa
            
        else:
            st.warning("Nenhum deputado encontrado com esse nome.")
            
    except requests.RequestException as e:
        st.error(f"Erro ao consultar a API: {e}")
