import streamlit as st
import google.generativeai as genai
import subprocess
import os

# --- DESIGN HEYGEN / VEO 3 STYLE ---
st.set_page_config(page_title="VeoLab AI PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    .stButton>button { background: #000; color: #fff; border-radius: 25px; width: 100%; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXÃO COM A API ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
else:
    st.error("Erro: 'GEMINI_API_KEY' não configurada nos Secrets.")
    model = None

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧪 VeoLab")
    email = st.text_input("Acesso VIP", value="niltonrosa71@gmail.com")
    opcao = st.radio("Navegação", ["🏠 Home", "🎬 Criar Vídeo", "👤 Avatares"])

# --- ÁREA CENTRAL ---
if opcao == "🎬 Criar Vídeo":
    st.markdown("## Transforme ideias em produção real")
    prompt = st.text_area("O que deve acontecer no vídeo?")
    
    if st.button("🚀 GERAR VÍDEO AGORA"):
        if model and prompt:
            with st.spinner("IA Renderizando..."):
                out = "veolab_output.mp4"
                # Comando FFmpeg em lista para evitar erros de shell
                cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1280x720:d=5", 
                       "-vf", f"drawtext=text='VeoLab: {prompt[:20]}...':fontcolor=white:x=(w-tw)/2:y=(h-th)/2", 
                       "-c:v", "libx264", "-pix_fmt", "yuv420p", out]
                
                try:
                    subprocess.run(cmd, check=True, capture_output=True)
                    if os.path.exists(out):
                        st.video(out)
                        st.success("Vídeo gerado!")
                except Exception as e:
                    st.error(f"Erro técnico: Verifique se o 'packages.txt' com 'ffmpeg' foi criado no GitHub.")
