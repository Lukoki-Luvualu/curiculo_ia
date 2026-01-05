import streamlit as st
from openai import OpenAI
from weasyprint import HTML
import os

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(
    page_title="Gerador de Currículo com IA",
    layout="wide"
)

st.title("🚀 Gerador de Currículo com IA")

# OpenAI Client (chave via Streamlit Secrets)
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

# ---------------- FUNÇÃO IA ----------------
@st.cache_data
def gerar_curriculo_ia(dados, area):
    prompt = f"""
    Gere um currículo profissional em português para a área de {area}.

    Dados do candidato:
    {dados}

    Estrutura:
    - Resumo Profissional
    - Experiência Profissional
    - Formação Acadêmica
    - Habilidades Técnicas

    Linguagem clara, profissional e otimizada para ATS.
    """

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return resposta.choices[0].message.content

# ---------------- FORMULÁRIO ----------------
with st.form("curriculo"):
    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome completo")
        email = st.text_input("Email")
        area = st.selectbox(
            "Área de Interesse",
            ["Desenvolvimento de Software", "Data Science", "Marketing Digital"]
        )

    with col2:
        experiencia = st.text_area("Experiência Profissional")
        formacao = st.text_area("Formação Acadêmica")
        habilidades = st.text_area("Habilidades")

    gerar = st.form_submit_button("✨ Gerar Currículo")

# ---------------- PROCESSAMENTO ----------------
if gerar:
    if not nome or not experiencia:
        st.error("Preencha pelo menos nome e experiência.")
    else:
        with st.spinner("🤖 Gerando currículo com IA..."):
            dados = f"""
            Nome: {nome}
            Email: {email}
            Experiência: {experiencia}
            Formação: {formacao}
            Habilidades: {habilidades}
            """

            conteudo = gerar_curriculo_ia(dados, area)

            st.success("Currículo gerado com sucesso!")
            st.markdown("### 📄 Currículo")
            st.text(conteudo)

            # ---------------- PDF ----------------
            html = f"""
            <html>
            <body style="font-family: Arial; padding: 40px;">
            <h1>{nome}</h1>
            <pre>{conteudo}</pre>
            </body>
            </html>
            """

            pdf = HTML(string=html).write_pdf()

            st.download_button(
                "📥 Baixar currículo em PDF",
                pdf,
                file_name="curriculo.pdf",
                mime="application/pdf"
            )
