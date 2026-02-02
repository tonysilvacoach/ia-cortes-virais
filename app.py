import streamlit as st
import google.generativeai as genai
import subprocess
import os

# --- INTERFACE PROFISSIONAL (HEYGEN STYLE) ---
st.set_page_config(page_title="VeoLab AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    .canvas-container { border: 1px solid #e2e8f0; border-radius: 12px; padding: 30px; background: white; text-align: center; }
    .stButton>button { background-color: #000000; color: white; border-radius: 20px; font-weight: 600; width: 100%; height: 3.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API (FORMATO TOML) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
else:
    st.error("⚠️ ERRO: Chave API não configurada nos Secrets. Use: GEMINI_API_KEY = 'SUA_CHAVE'")
    model = None

# --- SIDEBAR ASSETS ---
with st.sidebar:
    st.title("🧪 VeoLab")
    email = st.text_input("Identidade", value="niltonrosa71@gmail.com")
    st.write("---")
    menu = st.radio("Menu", ["🏠 Home", "🎬 Criar Vídeo", "👤 Avatares"])

# --- LÓGICA DE GERAÇÃO (CANVAS) ---
if menu == "🎬 Criar Vídeo":
    st.markdown("<h2 style='text-align: center;'>Transforme ideias em produção real</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
        tab_txt, tab_img = st.tabs(["✍️ Texto", "🖼️ Imagem"])
        
        with tab_txt:
            prompt = st.text_input("Descreva seu vídeo...", placeholder="Ex: Um pôr do sol na praia")
        with tab_img:
            img_file = st.file_uploader("Upload da imagem base", type=["jpg", "png"])

        if st.button("✨ GERAR VÍDEO AGORA"):
            if not prompt and not img_file:
                st.warning("Insira uma descrição ou imagem.")
            else:
                with st.spinner("VeoLab renderizando sua cena..."):
                    out_file = "veolab_final.mp4"
                    clean_prompt = prompt.replace("'", "").replace('"', "")[:30] # Limpa aspas para evitar erro de sintaxe
                    
                    # COMANDO FFmpeg CORRIGIDO: Remove conflitos de drawtext da Screenshot_31
                    cmd = [
                        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1280x720:d=5",
                        "-vf", f"drawtext=text='VeoLab Pro - {clean_prompt}':fontcolor=white:x=(w-tw)/2:y=(h-th)/2:fontsize=30",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", out_file
                    ]
                    
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        if result.returncode == 0 and os.path.exists(out_file):
                            st.video(out_file)
                            st.success("Vídeo produzido com sucesso!")
                        else:
                            st.error("Erro técnico na renderização.")
                            st.code(result.stderr) # Mostra o log real para debug profissional
                    except Exception as e:
                        st.error(f"Falha crítica no sistema: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Utilize o menu lateral para acessar as ferramentas de criação.")
