import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Título da aplicação
st.title("📊 Despesas dos Senadores - Dados Abertos do Senado Federal")

st.markdown("""
Digite o nome de um senador para visualizar o total de despesas por categoria, 
utilizando dados da [API pública da Codante](https://apis.codante.io/senator-expenses).
""")

# Entrada do nome do senador
nome_senador = st.text_input("Digite o nome do senador:")

if nome_senador:
    # Buscar todos os senadores
    url_senadores = "https://apis.codante.io/senator-expenses/senators"
    resposta = requests.get(url_senadores)

    if resposta.status_code == 200:
        senadores = resposta.json()

        # Procurar o senador pelo nome (case-insensitive)
        senador_encontrado = next(
            (s for s in senadores if nome_senador.lower() in s["name"].lower()), None
        )

        if senador_encontrado:
            senador_id = senador_encontrado["id"]
            st.success(f"Senador encontrado: **{senador_encontrado['name']}**")

            # Buscar despesas do senador
            url_despesas = f"https://apis.codante.io/senator-expenses/expenses?senatorId={senador_id}"
            resposta_despesas = requests.get(url_despesas)

            if resposta_despesas.status_code == 200:
                despesas = resposta_despesas.json()

                if despesas:
                    # Criar DataFrame
                    df = pd.DataFrame(despesas)

                    # Agrupar por categoria
                    despesas_categoria = df.groupby("category")["value"].sum().reset_index()

                    # Gráfico de barras
                    fig = px.bar(
                        despesas_categoria,
                        x="category",
                        y="value",
                        title=f"Despesas de {senador_encontrado['name']} por categoria",
                        labels={"category": "Categoria", "value": "Valor (R$)"},
                        text_auto=True,
                    )

                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)

                    # Mostrar tabela
                    with st.expander("Ver dados brutos"):
                        st.dataframe(df)
                else:
                    st.warning("Nenhuma despesa encontrada para esse senador.")
            else:
                st.error("Erro ao buscar as despesas do senador.")
        else:
            st.warning("Senador não encontrado. Verifique o nome e tente novamente.")
    else:
        st.error("Erro ao acessar a API dos senadores.")
else:
    st.info("Digite o nome de um senador para iniciar a busca.")
