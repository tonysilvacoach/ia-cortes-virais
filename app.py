import streamlit as st
import google.generativeai as genai
import subprocess
import os

# --- INTERFACE HEYGEN / VEO 3 STYLE ---
st.set_page_config(page_title="VeoLab AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    .canvas-container { border: 1px solid #e2e8f0; border-radius: 12px; padding: 30px; background: white; text-align: center; }
    .stButton>button { background-color: #000000; color: white; border-radius: 20px; font-weight: 600; width: 100%; height: 3rem; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API GEMINI ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
else:
    st.error("Erro: 'GEMINI_API_KEY' não encontrada nos Secrets.")
    model = None

# --- SIDEBAR (ASSETS) ---
with st.sidebar:
    st.title("🧪 VeoLab")
    email = st.text_input("Identidade", value="niltonrosa71@gmail.com")
    st.write("---")
    navegacao = st.radio("Menu", ["🏠 Home", "🎬 Criar Vídeo", "👤 Avatares"])

# --- ÁREA CENTRAL ---
if navegacao == "🏠 Home":
    st.markdown("<h2 style='text-align: center;'>Turn your ideas into production-ready video</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
        
        # Tabs para diferentes tipos de criação (Texto, Imagem, Audio)
        tab1, tab2, tab3 = st.tabs(["✍️ Texto", "🖼️ Imagem", "🎙️ Áudio"])
        
        with tab1:
            prompt = st.text_area("Descreva seu vídeo...", placeholder="Ex: Um apresentador de notícias em Formosa...")
        with tab2:
            img = st.file_uploader("Upload de imagem base", type=["jpg", "png"])
        with tab3:
            aud = st.file_uploader("Upload de áudio/narração", type=["mp3", "wav"])

        if st.button("✨ GERAR VÍDEO AGORA"):
            if model and (prompt or img or aud):
                with st.spinner("VeoLab AI está renderizando..."):
                    out_file = "veolab_prod.mp4"
                    
                    # Comando FFmpeg em lista para evitar erros de shell (Screenshot_19)
                    cmd = [
                        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1280x720:d=5",
                        "-vf", f"drawtext=text='VeoLab Pro - Gerando: {prompt[:20] if prompt else 'Midia'}...':fontcolor=white:x=(w-tw)/2:y=(h-th)/2:fontsize=30",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", out_file
                    ]
                    
                    try:
                        # Executa o comando e captura erros específicos (Screenshot_26)
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        if result.returncode == 0 and os.path.exists(out_file):
                            st.video(out_file)
                            st.success("Vídeo gerado com sucesso!")
                        else:
                            st.error(f"Falha na renderização: {result.stderr}")
                    except Exception as e:
                        st.error(f"Erro no motor de vídeo: {e}")
            else:
                st.warning("Insira um comando ou arquivo para gerar.")
        st.markdown('</div>', unsafe_allow_html=True)

elif navegacao == "👤 Avatares":
    st.subheader("Biblioteca de Avatares")
    st.info("Em breve: Clonagem de voz e imagem para os canais Notícias New e Habitus Milionário.")
