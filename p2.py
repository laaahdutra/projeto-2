import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Despesas dos Senadores", layout="wide")
st.title("📊 Despesas dos Senadores - Dados Abertos do Senado Federal")

st.markdown("""
Digite o nome de um senador para visualizar o total de despesas por categoria, 
utilizando dados da [API pública da Codante](https://apis.codante.io/senator-expenses).
""")

# Entrada do nome do senador
nome_senador = st.text_input("Digite o nome do senador:")

if nome_senador:
    url_senadores = "https://apis.codante.io/senator-expenses/senators"
    try:
        resposta = requests.get(url_senadores)
        resposta.raise_for_status()
        dados = resposta.json()

        # A API pode retornar uma lista ou um dicionário com 'data'
        senadores = dados.get("data", dados)

        # Procurar o senador pelo nome (ignora maiúsculas/minúsculas)
        senador_encontrado = next(
            (s for s in senadores if nome_senador.lower() in s["name"].lower()), None
        )

        if senador_encontrado:
            senador_id = senador_encontrado["id"]
            nome = senador_encontrado["name"]
            st.success(f"Senador encontrado: **{nome}**")

            url_despesas = f"https://apis.codante.io/senator-expenses/expenses?senatorId={senador_id}"

            try:
                resp_despesas = requests.get(url_despesas)
                resp_despesas.raise_for_status()
                dados_despesas = resp_despesas.json()

                despesas = dados_despesas.get("data", dados_despesas)

                if despesas:
                    df = pd.DataFrame(despesas)

                    # Alguns registros podem não ter valor ou categoria
                    df = df.dropna(subset=["category", "value"])

                    if not df.empty:
                        # Agrupar por categoria
                        resumo = df.groupby("category", as_index=False)["value"].sum()

                        fig = px.bar(
                            resumo,
                            x="category",
                            y="value",
                            title=f"Despesas de {nome} por categoria",
                            labels={"category": "Categoria", "value": "Valor (R$)"},
                            text_auto=".2s",
                        )
                        fig.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)

                        with st.expander("Ver dados completos"):
                            st.dataframe(df)
                    else:
                        st.warning("Nenhuma despesa com valores válidos encontrada.")
                else:
                    st.warning("Nenhuma despesa encontrada para esse senador.")
            except requests.RequestException as e:
                st.error(f"Erro ao buscar despesas: {e}")

        else:
            st.warning("Senador não encontrado. Verifique se o nome está correto.")

    except requests.RequestException as e:
        st.error(f"Erro ao conectar à API de senadores: {e}")

else:
    st.info("Digite o nome de um senador para iniciar a busca.")
