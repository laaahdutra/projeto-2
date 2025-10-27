# app.py
import streamlit as st
import requests

# Título da aplicação
st.title("Consulta de Deputados - Câmara dos Deputados")

# --- Parte 1: Consulta pelo nome do deputado ---
nome_deputado = st.text_input("Digite o nome do deputado:")

if nome_deputado:
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados?nome={nome_deputado}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        deputados = data.get("dados", [])
        
        if deputados:
            st.success(f"{len(deputados)} deputado(s) encontrado(s):")
            
            # Mostra informações do deputado
            for deputado in deputados:
                st.subheader(deputado.get("nome"))
                st.write(f"**ID:** {deputado.get('id')}")
                st.write(f"**Sigla Partido:** {deputado.get('siglaPartido')}")
                st.write(f"**UF:** {deputado.get('siglaUf')}")
                st.write(f"**URL Perfil:** [Link]({deputado.get('uri')})")
            
            # --- Parte 2: Consulta de despesas pelo ID ---
            st.markdown("---")
            st.subheader("Consultar despesas do deputado")
            id_deputado = st.text_input("Digite o ID do deputado para ver suas despesas:")
            
            if id_deputado:
                url_despesas = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_deputado}/despesas"
                
                try:
                    resp_despesas = requests.get(url_despesas, timeout=10)
                    despesas_data = resp_despesas.json()
                    
                    despesas = despesas_data.get("dados", [])
                    
                    if despesas:
                        st.success(f"{len(despesas)} despesa(s) encontrada(s):")
                        for despesa in despesas:
                            st.write(f"**Ano:** {despesa.get('ano')}")
                            st.write(f"**Mês:** {despesa.get('mes')}")
                            st.write(f"**Tipo:** {despesa.get('tipoDespesa')}")
                            st.write(f"**Valor:** R$ {despesa.get('valorDocumento')}")
                            st.write(f"**Descrição:** {despesa.get('descricao')}")
                            st.write("---")
                    else:
                        st.warning("Nenhuma despesa encontrada para este deputado.")
                        
                except requests.RequestException as e:
                    st.error(f"Erro ao consultar as despesas: {e}")
                    
        else:
            st.warning("Nenhum deputado encontrado com esse nome.")
            
    except requests.RequestException as e:
        st.error(f"Erro ao consultar a API: {e}")
