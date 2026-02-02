import streamlit as st
import google.generativeai as genai
import subprocess
import os

# --- INTERFACE PREMIUM (HEYGEN/VEO 3 STYLE) ---
st.set_page_config(page_title="VeoLab AI PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    .canvas-container { border: 1px solid #e2e8f0; border-radius: 12px; padding: 30px; background: white; text-align: center; }
    .stButton>button { background-color: #000000; color: white; border-radius: 20px; font-weight: 600; width: 100%; height: 3.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA DA API ---
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-pro')
    except Exception as e:
        st.error(f"Erro ao configurar IA: {e}")
else:
    st.error("ERRO: Chave 'GEMINI_API_KEY' não encontrada nos Secrets.")

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🧪 VeoLab")
    st.write(f"Usuário: {st.text_input('Login', value='niltonrosa71@gmail.com')}")
    aba = st.radio("Menu", ["🏠 Home", "🎬 Criar Vídeo", "👤 Avatares"])

# --- ÁREA DE CRIAÇÃO ---
if aba == "🎬 Criar Vídeo":
    st.markdown("<h2 style='text-align: center;'>Transforme ideias em produção real</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
        prompt = st.text_area("Descreva seu vídeo (Texto, Imagem ou Áudio)...", placeholder="Ex: Um pôr do sol em Formosa-GO")
        
        if st.button("✨ GERAR VÍDEO AGORA"):
            if model and prompt:
                with st.spinner("IA interpretando e renderizando..."):
                    # 1. IA gera o roteiro
                    try:
                        res = model.generate_content(f"Descreva em 1 frase curta uma cena visual para: {prompt}")
                        descricao_ia = res.text
                        
                        # 2. Renderização FFmpeg (Resolvendo erro de aspas e argumentos)
                        out = "veolab_prod.mp4"
                        clean_text = descricao_ia.replace("'", "").replace('"', "")[:40]
                        
                        cmd = [
                            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1280x720:d=5",
                            "-vf", f"drawtext=text='{clean_text}':fontcolor=white:x=(w-tw)/2:y=(h-th)/2:fontsize=30",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", out
                        ]
                        
                        subprocess.run(cmd, check=True, capture_output=True)
                        
                        if os.path.exists(out):
                            st.video(out)
                            st.success("Vídeo produzido com sucesso!")
                    except Exception as e:
                        st.error(f"Falha na geração: {e}")
            else:
                st.warning("Verifique a API Key ou o Prompt.")
        st.markdown('</div>', unsafe_allow_html=True)
