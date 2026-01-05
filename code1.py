import streamlit as st
from openai import OpenAI
import io
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from weasyprint import HTML, CSS
import base64

# Configuração OpenAI (substitua pela sua chave)
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", "sua-chave-aqui"))

@st.cache_data
def gerar_curriculo_ia(dados, area_interesse):
    """Analisa dados e gera conteúdo otimizado com IA"""
    prompt = f"""
    Analise estes dados e gere um currículo PROFISSIONAL em PORTUGUÊS otimizado para a área de {area_interesse}:
    
    Dados: {dados}
    
    Gere em FORMATO ESTRUTURADO (apenas texto, sem markdown):
    1. RESUMO PROFISSIONAL (3-4 linhas impactantes)
    2. EXPERIÊNCIA PROFISSIONAL (formato: Cargo | Empresa | Período | 3 conquistas com números)
    3. FORMAÇÃO ACADÊMICA (Instituição | Curso | Ano)
    4. HABILIDADES TÉCNICAS (5-8 principais para a área)
    5. CERTIFICAÇÕES (se houver)
    
    Use linguagem ativa, verbos de ação e otimize para ATS (palavras-chave da área).
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def criar_pdf_html(nome, conteudo):
    """Gera PDF moderno via HTML/CSS"""
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ margin: 2cm; }}
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.4; color: #2c3e50; max-width: 210mm; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2cm 2.5cm 1.5cm; }}
            .nome {{ font-size: 32px; font-weight: 700; margin: 0; letter-spacing: 2px; }}
            .contato {{ font-size: 12px; margin-top: 8px; opacity: 0.9; }}
            .section {{ margin: 2cm 2.5cm 1.5cm; }}
            .section-title {{ font-size: 18px; font-weight: 600; color: #667eea; border-bottom: 3px solid #667eea; padding-bottom: 8px; margin-bottom: 1cm; }}
            .experiencia-item {{ margin-bottom: 1.2cm; }}
            .cargo {{ font-size: 14px; font-weight: 600; color: #2c3e50; }}
            .empresa {{ font-size: 12px; color: #7f8c8d; }}
            .descricao {{ font-size: 11px; margin-top: 4px; }}
            .habilidades {{ display: flex; flex-wrap: wrap; gap: 8px; }}
            .skill {{ background: #ecf0f1; padding: 6px 12px; border-radius: 20px; font-size: 11px; font-weight: 500; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1 class="nome">{nome}</h1>
            <div class="contato">📧 contato@email.com | 📱 (11) 99999-9999 | 🔗 linkedin.com/in/{nome.lower().replace(' ', '-')}</div>
        </div>
        
        <div class="section">
            <div class="section-title">📋 Resumo Profissional</div>
            <div style="font-size: 12px; line-height: 1.6;">{conteudo.split('1. RESUMO PROFISSIONAL')[1].split('2.')[0].strip()}</div>
        </div>
        
        <div class="section">
            <div class="section-title">💼 Experiência Profissional</div>
            <div>{conteudo.split('2. EXPERIÊNCIA PROFISSIONAL')[1].split('3.')[0].strip()}</div>
        </div>
        
        <div class="section">
            <div class="section-title">🎓 Formação Acadêmica</div>
            <div>{conteudo.split('3. FORMAÇÃO ACADÊMICA')[1].split('4.')[0].strip()}</div>
        </div>
        
        <div class="section">
            <div class="section-title">🛠️ Habilidades Técnicas</div>
            <div class="habilidades">{conteudo.split('4. HABILIDADES TÉCNICAS')[1].split('5.')[0].strip()}</div>
        </div>
    </body>
    </html>
    """
    
    html = HTML(string=html_template)
    pdf_bytes = html.write_pdf()
    return pdf_bytes

# Interface Streamlit
st.set_page_config(page_title="AI Currículo Generator", layout="wide")
st.title("🚀 Gerador de Currículos com IA")
st.markdown("---")

# Formulário de entrada
col1, col2 = st.columns([1, 1])

with col1:
    nome = st.text_input("👤 Nome Completo", "João Silva")
    email = st.text_input("📧 Email")
    telefone = st.text_input("📱 Telefone")
    linkedin = st.text_input("🔗 LinkedIn")
    area = st.selectbox("🎯 Área de Interesse", 
                       ["Desenvolvimento de Software", "Data Science", "Marketing Digital", 
                        "Gestão de Projetos", "DevOps", "Cybersecurity", "Design UX/UI"])

with col2:
    st.subheader("📝 Dados Profissionais")
    experiencia = st.text_area("Experiência (copie e cole)", 
                              "Desenvolvedor Python na TechCorp (2021-2024)\nAnalista de Dados na DataInc (2019-2021)")
    formacao = st.text_area("Formação Acadêmica", 
                           "Bacharel em Ciência da Computação - USP (2015-2019)\nCurso React - Alura (2023)")
    habilidades = st.text_area("Habilidades", "Python, JavaScript, Docker, AWS, SQL, Git")

# Botão Gerar
if st.button("✨ Gerar Currículo com IA", type="primary"):
    with st.spinner("🤖 IA analisando e otimizando seu currículo..."):
        dados = f"""
        Nome: {nome}
        Contato: {email}, {telefone}, {linkedin}
        Experiência: {experiencia}
        Formação: {formacao}
        Habilidades: {habilidades}
        """
        
        conteudo_otimizado = gerar_curriculo_ia(dados, area)
        
        # Gera PDF
        pdf_bytes = criar_pdf_html(nome, conteudo_otimizado)
        
        # Download
        st.success("✅ Currículo gerado com sucesso!")
        st.balloons()
        
        st.download_button(
            label="📥 Download PDF",
            data=pdf_bytes,
            file_name=f"Curriculo_{nome.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
        
        # Preview
        st.markdown("### 👀 Preview:")
        st.markdown(conteudo_otimizado)

st.markdown("---")
st.caption("💡 Dica: Preencha todos os campos para melhor resultado da IA")
