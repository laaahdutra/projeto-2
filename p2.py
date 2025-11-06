import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Consulta de Deputados - Câmara", layout="wide")

st.title("Consulta de Deputados - Câmara dos Deputados")

nome_deputado = st.text_input("Digite o nome do deputado:")

if nome_deputado:
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados"
    params = {"nome": nome_deputado, "itens": 100}  # buscar até 100 resultados de uma vez
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao consultar a API de deputados: {e}")
        st.stop()

    deputados = data.get("dados", [])
    if deputados:
        st.success(f"{len(deputados)} deputado(s) encontrado(s):")
        for deputado in deputados:
            st.subheader(deputado.get("nome"))
            st.write(f"*ID:* {deputado.get('id')}")
            st.write(f"*Sigla Partido:* {deputado.get('siglaPartido')}")
            st.write(f"*UF:* {deputado.get('siglaUf')}")
            st.write(f"*URL Perfil:* [Link]({deputado.get('uri')})")
    else:
        st.warning("Nenhum deputado encontrado com esse nome.")

st.markdown("---")
st.subheader("Consultar despesas do deputado")
id_deputado = st.text_input("Digite o ID do deputado para ver suas despesas:")

if id_deputado:
    
    id_clean = id_deputado.strip()
    if not id_clean.isdigit():
        st.error("ID inválido: informe apenas números correspondentes ao ID do deputado.")
    else:
        base_url = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_clean}/despesas"
        despesas = []
        pagina = 1

        try:
            while True:
                params = {"pagina": pagina, "itens": 100}  # 100 por página (máximo)
                resp = requests.get(base_url, params=params, timeout=15)
                resp.raise_for_status()
                despesas_data = resp.json()

                dados_pagina = despesas_data.get("dados", [])
                if not dados_pagina:
                    break

                despesas.extend(dados_pagina)
                
                pagina += 1

            if despesas:
                st.success(f"{len(despesas)} despesa(s) encontrada(s) para o deputado {id_clean}.")

                df = pd.DataFrame(despesas)

                if "valorDocumento" in df.columns:
                   
                    df["valorDocumento"] = (
                        df["valorDocumento"]
                        .astype(str)
                        .str.replace(".", "", regex=False)
                        .str.replace(",", ".", regex=False)
                    )
                    df["valorDocumento"] = pd.to_numeric(df["valorDocumento"], errors="coerce").fillna(0)
                else:
                    
                    df["valorDocumento"] = 0

                colunas_desejadas = ["ano", "mes", "tipoDespesa", "valorDocumento", "fornecedor", "descricao"]
                colunas_existentes = [col for col in colunas_desejadas if col in df.columns]

                if colunas_existentes:
                    st.dataframe(df[colunas_existentes].sort_values(by=["ano", "mes"], ascending=[False, False]))
                else:
                    st.warning("Não há colunas esperadas disponíveis para exibição.")

                st.markdown("📊 Gráfico de Despesas")

                if not df.empty:
                   
                    if "tipoDespesa" in df.columns:
                        grafico_tipo = df.groupby("tipoDespesa")["valorDocumento"].sum().sort_values(ascending=False)
                        if not grafico_tipo.empty:
                            st.bar_chart(grafico_tipo)
                        else:
                            st.info("Sem dados para gerar o gráfico por tipo de despesa.")
                    else:
                        st.info("Coluna 'tipoDespesa' não disponível para gerar gráfico.")

                   
                    if "mes" in df.columns and "ano" in df.columns:
                        # cria período para ordenar (ano-mês)
                        df["periodo"] = df["ano"].astype(str) + "-" + df["mes"].astype(str).str.zfill(2)
                        grafico_mes = df.groupby("periodo")["valorDocumento"].sum().sort_index()
                        if not grafico_mes.empty:
                            st.line_chart(grafico_mes)
                        else:
                            st.info("Sem dados para gerar o gráfico mensal.")
                    elif "mes" in df.columns:
                        grafico_mes = df.groupby("mes")["valorDocumento"].sum().sort_index()
                        if not grafico_mes.empty:
                            st.line_chart(grafico_mes)
                        else:
                            st.info("Sem dados para gerar o gráfico mensal.")
                    else:
                        st.info("Coluna 'mes' não disponível para gerar gráfico.")
                else:
                    st.warning("Não foi possível gerar gráficos — dados vazios.")
            else:
                st.warning("Nenhuma despesa encontrada para este deputado.")
        except requests.RequestException as e:
            st.error(f"Erro ao consultar as despesas: {e}") 
