import streamlit as st
import google.generativeai as genai
import subprocess
import os

# --- INTERFACE HEYGEN / VEO 3 STYLE ---
st.set_page_config(page_title="VeoLab AI PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    .canvas { border: 1px solid #e2e8f0; border-radius: 12px; padding: 40px; text-align: center; background: white; }
    .stButton>button { background: #000; color: #fff; border-radius: 20px; font-weight: bold; width: 100%; height: 3.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DA API (FIX 400) ---
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-pro')
    except Exception as e:
        st.error(f"Erro na API: {e}")
else:
    st.error("ERRO: 'GEMINI_API_KEY' não encontrada nos Secrets.")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧪 VeoLab")
    st.write(f"Usuário: {st.text_input('Login', value='niltonrosa71@gmail.com')}")
    aba = st.radio("Menu", ["🏠 Home", "🎬 Criar Vídeo"])

# --- ÁREA DE CRIAÇÃO ---
if aba == "🎬 Criar Vídeo":
    st.markdown("<h2 style='text-align: center;'>Gerador Multimídia VeoLab</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="canvas">', unsafe_allow_html=True)
        prompt = st.text_area("Descreva sua cena (Texto, Imagem ou Áudio)...")
        
        if st.button("🚀 GERAR VÍDEO AGORA"):
            if model and prompt:
                with st.spinner("IA processando sua ideia..."):
                    try:
                        # 1. IA cria a descrição curta
                        res = model.generate_content(f"Crie uma frase curta visual para: {prompt}")
                        descricao = res.text.replace("'", "").replace('"', "")[:40]
                        
                        # 2. Renderização (Resolvendo erro Screenshot_31)
                        out = "veolab_prod.mp4"
                        cmd = [
                            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1280x720:d=5",
                            "-vf", f"drawtext=text='{descricao}':fontcolor=white:x=(w-tw)/2:y=(h-th)/2:fontsize=30",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", out
                        ]
                        
                        subprocess.run(cmd, check=True, capture_output=True)
                        if os.path.exists(out):
                            st.video(out)
                            st.success("Vídeo gerado com sucesso!")
                    except Exception as e:
                        st.error(f"Falha na geração: {e}")
            else:
                st.warning("Verifique sua API Key ou o Prompt.")
        st.markdown('</div>', unsafe_allow_html=True)
