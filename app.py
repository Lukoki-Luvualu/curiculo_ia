import streamlit as st
from openai import OpenAI
from weasyprint import HTML

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(
    page_title="Gerador de Currículo com IA",
    layout="wide"
)

st.title("🚀 Gerador de Currículo com IA")
st.caption("Crie um currículo profissional em minutos com Inteligência Artificial")

# OpenAI (via Secrets)
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

# ---------------- FUNÇÃO IA (PROMPT OTIMIZADO) ----------------
@st.cache_data
def gerar_curriculo_ia(dados, area):
    prompt = f"""
    Você é um recrutador profissional e especialista em ATS.

    Crie um currículo PROFISSIONAL em PORTUGUÊS para a área de {area}.

    Use linguagem clara, objetiva, com verbos de ação.
    Destaque resultados e competências.
    Não use emojis.

    Estrutura obrigatória:
    RESUMO PROFISSIONAL (3 linhas)
    EXPERIÊNCIA PROFISSIONAL (cargo | empresa | período | 3 resultados)
    FORMAÇÃO ACADÊMICA
    HABILIDADES TÉCNICAS

    Dados do candidato:
    {dados}
    """

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25
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
            [
                "Desenvolvimento de Software",
                "Data Science",
                "Marketing Digital",
                "Gestão de Projetos"
            ]
        )

    with col2:
        experiencia = st.text_area("Experiência Profissional")
        formacao = st.text_area("Formação Acadêmica")
        habilidades = st.text_area("Habilidades Técnicas")

    gerar = st.form_submit_button("✨ Gerar Currículo")

# ---------------- PROCESSAMENTO ----------------
if gerar:
    if not nome or not experiencia:
        st.error("Preencha pelo menos o nome e a experiência.")
    else:
        with st.spinner("🤖 Gerando currículo profissional..."):
            dados = f"""
            Nome: {nome}
            Email: {email}
            Experiência: {experiencia}
            Formação: {formacao}
            Habilidades: {habilidades}
            """

            conteudo = gerar_curriculo_ia(dados, area)

            st.success("Currículo gerado com sucesso!")
            st.text(conteudo)

            # ---------------- PDF PROFISSIONAL ----------------
            html = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial;
                        padding: 40px;
                        line-height: 1.5;
                    }}
                    h1 {{
                        border-bottom: 2px solid #333;
                        padding-bottom: 10px;
                    }}
                </style>
            </head>
            <body>
                <h1>{nome}</h1>
                <pre>{conteudo}</pre>
            </body>
            </html>
            """

            pdf = HTML(string=html).write_pdf()

            st.download_button(
                "📥 Baixar currículo em PDF",
                pdf,
                file_name="curriculo_profissional.pdf",
                mime="application/pdf"
            )