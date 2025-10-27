# ========================================
# GERADOR DE PETIÇÃO AUTOMÁTICA - STREAMLIT
# Base jurídica: arts. 319 e seguintes do CPC
# Autora: Lara Ivo Barros Dutra
# ========================================

import streamlit as st
from datetime import date

# Função que gera o texto da petição
def gerar_peticao(nome_autor, nome_reu, tipo_acao, comarca, pedidos, valor_causa):
    data_hoje = date.today().strftime("%d/%m/%Y")

    peticao = f"""
EXCELENTÍSSIMO(A) SENHOR(A) JUIZ(A) DE DIREITO DA {comarca.upper()}

{nome_autor.upper()}, brasileiro(a), portador(a) de CPF nº XXX.XXX.XXX-XX,
residente e domiciliado(a) nesta cidade, por intermédio de seu advogado (instrumento de mandato anexo),
vem, respeitosamente, à presença de Vossa Excelência propor a presente

AÇÃO DE {tipo_acao.upper()}

em face de {nome_reu.upper()}, brasileiro(a), portador(a) de CPF nº XXX.XXX.XXX-XX,
pelos fatos e fundamentos jurídicos que passa a expor:

I - DOS FATOS
O autor expõe, em síntese, os fatos que motivam a presente demanda. 
(Descreva aqui, se desejar, os fatos de forma resumida.)

II - DO DIREITO
O pedido fundamenta-se no Código Civil e no Código de Processo Civil, 
especialmente nos arts. 186 e 927 do Código Civil, e art. 319 do CPC, 
bem como na jurisprudência pátria aplicável à espécie.

III - DOS PEDIDOS
Diante do exposto, requer:
{pedidos}

Dá-se à causa o valor de R$ {valor_causa:,.2f}.

Nestes termos,
Pede deferimento.

{comarca}, {data_hoje}.

__________________________________________
Advogado(a)
OAB/XX 000000
"""
    return peticao


# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Gerador de Petição", page_icon="⚖️")
st.title("⚖️ Gerador Automático de Petição Inicial")
st.write("Preencha as informações abaixo e gere automaticamente uma petição conforme o art. 319 do CPC.")

# Formulário
with st.form("form_peticao"):
    nome_autor = st.text_input("Nome do Autor")
    nome_reu = st.text_input("Nome do Réu")
    tipo_acao = st.text_input("Tipo de Ação (ex: indenização por danos morais)")
    comarca = st.text_input("Comarca (ex: Comarca de Belo Horizonte/MG)")
    pedidos = st.text_area("Pedidos Principais", 
                           "1. A citação do réu;\n2. A procedência da ação;\n3. A condenação em custas e honorários.")
    valor_causa = st.number_input("Valor da causa (em R$)", min_value=0.0, step=100.0)
    
    gerar = st.form_submit_button("🧾 Gerar Petição")

# Quando o botão for clicado
if gerar:
    if not nome_autor or not nome_reu or not tipo_acao or not comarca:
        st.warning("⚠️ Preencha todos os campos obrigatórios.")
    else:
        peticao = gerar_peticao(nome_autor, nome_reu, tipo_acao, comarca, pedidos, valor_causa)
        st.success("✅ Petição gerada com sucesso!")

        st.download_button(
            label="📥 Baixar Petição em TXT",
            data=peticao,
            file_name=f"peticao_{nome_autor.lower().replace(' ', '_')}.txt",
            mime="text/plain"
        )

        st.divider()
        st.subheader("📄 Prévia da Petição:")
        st.text_area("Visualização", peticao, height=400)
