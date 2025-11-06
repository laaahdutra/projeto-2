import streamlit as st
import requests
import pandas as pd
import plotly.express as px

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

        # Pode vir como {"data": [...]}
        senadores = dados.get("data", dados)

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

                    # Mostrar as colunas para depuração
                    st.write("🔍 Colunas retornadas pela API:", list(df.columns))

                    # Normaliza nomes de colunas caso venham diferentes
                    col_categoria = None
                    col_valor = None

                    for c in df.columns:
                        if "category" in c.lower() or "expense_type" in c.lower():
                            col_categoria = c
                        if "value" in c.lower() or "amount" in c.lower():
                            col_valor = c

                    if col_categoria and col_valor:
                        df = df.dropna(subset=[col_categoria, col_valor])

                        resumo = (
                            df.groupby(col_categoria, as_index=False)[col_valor]
                            .sum()
                            .sort_values(by=col_valor, ascending=False)
                        )

                        fig = px.bar(
                            resumo,
                            x=col_categoria,
                            y=col_valor,
                            title=f"Despesas de {nome} por categoria",
                            labels={col_categoria: "Categoria", col_valor: "Valor (R$)"},
                            text_auto=".2s",
                        )
                        fig.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)

                        with st.expander("Ver dados completos"):
                            st.dataframe(df)
                    else:
                        st.warning(
                            "A API retornou dados, mas não há colunas de categoria/valor identificáveis."
                        )
                        st.dataframe(df)
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
