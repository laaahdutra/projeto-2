# app.py
import streamlit as st
import requests

st.title("Consulta de Deputados - Câmara dos Deputados")

nome_deputado = st.text_input("Digite o nome do deputado:")

if nome_deputado:
    # Busca informações do deputado
    url_deputado = f"https://dadosabertos.camara.leg.br/api/v2/deputados?nome={nome_deputado}"
    try:
        response = requests.get(url_deputado, timeout=10)
        data = response.json()
        deputados = data.get("dados", [])
        
        if deputados:
            st.subheader("Resultados da busca:")
            for deputado in deputados:
                st.write(f"**Nome:** {deputado.get('nome')}")
                st.write(f"**ID:** {deputado.get('id')}")
                st.write(f"**Sigla do Partido:** {deputado.get('siglaPartido')}")
                st.write(f"**UF:** {deputado.get('siglaUf')}")
                
                # Busca despesas do deputado
                url_despesas = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{deputado.get('id')}/despesas"
                try:
                    desp_response = requests.get(url_despesas, timeout=10)
                    despesas_data = desp_response.json()
                    despesas = despesas_data.get("dados", [])
                    
                    if despesas:
                        st.write("**Despesas recentes:**")
                        for desp in despesas[:5]:  # mostra apenas as 5 primeiras
                            st.write(f"- {desp.get('tipoDespesa')}: R$ {desp.get('valorDocumento')}")
                    else:
                        st.write("Nenhuma despesa encontrada.")
                        
                except requests.RequestException as e:
                    st.error(f"Erro ao buscar despesas: {e}")
                
                st.markdown("---")
        else:
            st.warning("Nenhum deputado encontrado com esse nome.")
            
    except requests.RequestException as e:
        st.error(f"Erro ao consultar a API: {e}")

