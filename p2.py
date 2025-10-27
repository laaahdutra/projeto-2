import pandas as pd
import streamlit as px

def baixar_dados(url: str, local_arquivo: str = "infopen.csv") -> None:
    """
    Faz o download dos dados da URL para um arquivo CSV local.
    """
    df = pd.read_csv(url, low_memory=False)
    df.to_csv(local_arquivo, index=False)
    print(f"Arquivo salvo como {local_arquivo}")

def preparar_dados(local_arquivo: str = "infopen.csv") -> pd.DataFrame:
    """
    Lê o arquivo CSV, filtra para obter os dados agregados por estado (UF)
    e extrai as colunas relevantes: sigla da UF e população carcerária.
    """
    df = pd.read_csv(local_arquivo, low_memory=False)
    # Exemplos de colunas que podem existir – ajusta conforme o dataset real
    # Vamos filtrar para “população prisional” por UF
    # Supomos as colunas: 'UF', 'POPULACAO_PRISIONAL' (nome fictício, verifique no dataset real)
    col_uf = 'UF'
    col_pop = 'POPULACAO_PRISIONAL'
    if col_uf not in df.columns or col_pop not in df.columns:
        print("ATENÇÃO: colunas esperadas não encontradas. Veja os nomes das colunas no dataset.")
        print("Colunas disponíveis:", df.columns.tolist())
        # Para continuar, vamos supor que haja uma coluna chamada 'SIGLA_UF' e 'TOTAL_PRESOS'
        col_uf = 'SIGLA_UF'
        col_pop = 'TOTAL_PRESOS'
    # Fazer agrupamento por UF
    df2 = df.groupby(col_uf)[col_pop].sum().reset_index()
    df2 = df2.rename(columns={col_uf: 'sigla', col_pop: 'populacao_carceraria'})
    # Opcional: remover linhas com sigla inválida ou NaN
    df2 = df2.dropna(subset=['sigla', 'populacao_carceraria'])
    return df2

def gerar_mapa(df: pd.DataFrame, titulo: str = "População Carcerária por Estado (Brasil)") -> None:
    """
    Gera mapa coroplético da população carcerária por estado (sigla).
    """
    fig = px.choropleth(
        df,
        locations='sigla',
        locationmode='USA-states' if False else 'ISO-ALPHA-2',  # modifique se necessário; para Brasil pode requerer geojson
        color='populacao_carceraria',
        hover_name='sigla',
        color_continuous_scale='Reds',
        title=titulo
    )
    # Ajustes para exibir o mapa
    fig.update_geos(fitbounds="locations", visible=False)
    fig.show()

def main():
    url = "http://dados.mj.gov.br/dataset/f9ebf1f1-8d27-4937-b330-f29b820dca87/resource/54cdab5b-b241-4dcc-83af-43cba0250ef3/download/copia-de-dadosformularios-jan-jun2019.csv"
    arquivo_local = "infopen.csv"
    print("Baixando dados …")
    baixar_dados(url, arquivo_local)
    print("Preparando dados …")
    df_estados = preparar_dados(arquivo_local)
    print("Gerando mapa …")
    gerar_mapa(df_estados)

if __name__ == "__main__":
    main()
