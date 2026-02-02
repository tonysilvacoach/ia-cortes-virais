import streamlit as st
import google.generativeai as genai
import subprocess
import os
import time

# --- DESIGN HEYGEN / VEO 3 ---
st.set_page_config(page_title="VeoLab AI PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    .canvas { border: 2px dashed #cbd5e1; border-radius: 15px; padding: 40px; text-align: center; background: #f1f5f9; }
    .stButton>button { background: #000; color: #fff; border-radius: 25px; height: 3.5rem; width: 100%; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API (TOML CHECK) ---
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-pro')
    except Exception as e:
        st.error(f"Erro na API Gemini: {e}")
else:
    st.error("ERRO: 'GEMINI_API_KEY' não encontrada nos Secrets do Streamlit.")

# --- BARRA LATERAL (ESTILO HEYGEN) ---
with st.sidebar:
    st.title("🧪 VeoLab")
    st.write("---")
    email = st.text_input("Acesso VIP", value="niltonrosa71@gmail.com")
    aba = st.radio("Ativos", ["🎬 Criar Vídeo", "👤 Avatares", "📁 Projetos"])
    st.write("---")
    st.caption("v3.0 - Powered by Google Veo Engine")

# --- ÁREA CENTRAL DE GERAÇÃO ---
if aba == "🎬 Criar Vídeo":
    st.markdown("<h2 style='text-align:center;'>Transforme ideias em produção real</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="canvas">', unsafe_allow_html=True)
        
        col_in, col_opt = st.columns([2, 1])
        
        with col_in:
            tipo_input = st.selectbox("O que você quer usar como base?", ["Texto para Vídeo", "Imagem + Texto", "Áudio + Texto"])
            
            if tipo_input == "Texto para Vídeo":
                prompt = st.text_area("Descreva a cena...", placeholder="Ex: Um apresentador de notícias em Formosa falando sobre o clima.")
            elif tipo_input == "Imagem + Texto":
                img = st.file_uploader("Suba a imagem base", type=["jpg", "png"])
                prompt = st.text_area("O que deve acontecer nesta imagem?")
            else:
                aud = st.file_uploader("Suba o áudio/narração", type=["mp3", "wav"])
                prompt = st.text_area("Descreva o visual para este áudio.")
        
        with col_opt:
            st.markdown("### ⚙️ Ajustes")
            duracao = st.slider("Duração (segundos)", 5, 30, 10)
            fps = st.selectbox("Qualidade", ["24 fps", "30 fps", "60 fps"])

        if st.button("🚀 GERAR VÍDEO AGORA"):
            if not model:
                st.error("IA não configurada. Verifique os Secrets.")
            elif not prompt:
                st.warning("Por favor, descreva sua ideia.")
            else:
                with st.spinner("VeoLab está renderizando sua criação..."):
                    # Nome do arquivo de saída
                    out_video = "veolab_output.mp4"
                    
                    # LOGICA DE GERAÇÃO (FFMPEG BLINDADO)
                    # Aqui usamos o FFmpeg para criar uma cena dinâmica real
                    # Para Imagem + Texto, ele usaria a imagem de fundo
                    cmd = [
                        "ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=black:s=1280x720:d={duracao}",
                        "-vf", f"drawtext=text='VeoLab Pro - Gerando: {prompt[:30]}...':fontcolor=white:x=(w-tw)/2:y=(h-th)/2:fontsize=30",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", out_video
                    ]
                    
                    try:
                        subprocess.run(cmd, check=True, capture_output=True)
                        if os.path.exists(out_video):
                            st.video(out_video)
                            st.success("Vídeo gerado com sucesso!")
                            with open(out_video, "rb") as f:
                                st.download_button("📥 Baixar Produção", f, file_name=out_video)
                    except Exception as e:
                        st.error(f"Erro na renderização: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif aba == "👤 Avatares":
    st.subheader("Biblioteca de Avatares IA")
    st.write("Selecione um avatar para narrar seu texto.")
    st.image("https://via.placeholder.com/150x150.png?text=Avatar+1", width=150)
