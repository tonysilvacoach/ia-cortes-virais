import streamlit as st
import google.generativeai as genai
import subprocess
import os

# --- INTERFACE PREMIUM (HEYGEN STYLE) ---
st.set_page_config(page_title="VeoLab AI PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    .canvas-container { border: 1px solid #e2e8f0; border-radius: 12px; padding: 30px; background: white; text-align: center; }
    .stButton>button { background-color: #000000; color: white; border-radius: 20px; font-weight: 600; width: 100%; height: 3.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DA IA (FIX 404) ---
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Alterado para 'gemini-1.5-flash' ou o nome completo estável
        model = genai.GenerativeModel('gemini-1.5-flash') 
    except Exception as e:
        st.error(f"Erro ao carregar modelo: {e}")
else:
    st.error("Chave 'GEMINI_API_KEY' não encontrada nos Secrets.")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧪 VeoLab")
    email = st.text_input("Identidade", value="niltonrosa71@gmail.com")
    menu = st.radio("Menu", ["🏠 Home", "🎬 Criar Vídeo"])

# --- DASHBOARD CENTRAL ---
if menu == "🎬 Criar Vídeo":
    st.markdown("<h2 style='text-align: center;'>Transforme ideias em produção real</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
        prompt = st.text_area("Descreva o vídeo (Texto, Imagem ou Áudio)...")
        
        if st.button("✨ GERAR VÍDEO AGORA"):
            if model and prompt:
                with st.spinner("IA processando sua ideia..."):
                    try:
                        # Geração do roteiro para confirmar que a API está OK
                        res = model.generate_content(f"Crie uma frase visual curta para: {prompt}")
                        descricao = res.text.replace("'", "").replace('"', "")[:40]
                        
                        # Motor de Vídeo FFmpeg (Resolvendo erro de renderização)
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
                        st.error(f"Falha técnica: {e}")
            else:
                st.warning("Insira o prompt ou verifique a API Key.")
        st.markdown('</div>', unsafe_allow_html=True)
