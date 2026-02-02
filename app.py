import streamlit as st
import google.generativeai as genai
import subprocess
import os
import io
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA: ESTILO VEOLAB ---
st.set_page_config(page_title="VeoLab AI - Gerador de Vídeos", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp { background-color: #0c0c0c; color: #f0f0f0; font-family: 'Inter', sans-serif; }
    
    /* Título Central VeoLab */
    .veolab-title {
        font-size: 3.2rem; font-weight: 700;
        text-align: center; margin-bottom: 2rem;
        background: linear-gradient(90deg, #4F8BF9, #EC4899);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .veolab-subtitle {
        text-align: center; color: #a0a0a0; font-size: 1.1rem; margin-bottom: 3rem;
    }

    /* Cards de Input/Output */
    .veolab-card {
        background: #1a1a1a; border: 1px solid #2a2a2a;
        border-radius: 8px; padding: 25px; height: 100%;
    }

    /* Botão de Geração */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: white; border: none; border-radius: 6px;
        padding: 12px 25px; font-weight: 600;
        font-size: 1.1rem; width: 100%;
        margin-top: 20px;
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 5px 15px rgba(168, 85, 247, 0.3); }

    /* Sidebar minimalista */
    [data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid #111111;
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DO GEMINI API ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"⚠️ Erro na configuração da API Gemini: {e}. Verifique sua GEMINI_API_KEY nas Secrets do Streamlit.")
    model = None # Garante que o modelo não seja usado se houver erro

# --- ACESSO PROPRIETÁRIO (Seu e-mail) ---
PROPRIETARIO = "niltonrosa71@gmail.com"

with st.sidebar:
    st.markdown("<h2 style='color:#ffffff;'>VeoLab</h2>", unsafe_allow_html=True)
    user_email = st.text_input("Identidade", placeholder="seu@email.com")
    is_admin = (user_email.lower() == PROPRIETARIO.lower()) if user_email else False
    st.write("---")
    st.caption(f"Status: {'👑 PRO' if is_admin else '✨ Gratuito'}")
    st.markdown("---")
    if not is_admin:
        st.info("Plano Gratuito: Limite de 1 geração por sessão.")
        if st.button("💎 Upgrade para VeoLab PRO"):
            st.warning("Funcionalidade de upgrade em breve!")

# --- TÍTULOS VEOLAB ---
st.markdown("<div class='veolab-title'>VeoLab AI</div>", unsafe_allow_html=True)
st.markdown("<div class='veolab-subtitle'>Gere vídeos incríveis a partir de Texto, Imagem ou Áudio.</div>", unsafe_allow_html=True)

# --- ÁREA DE ENTRADA MULTIMÍDIA ---
col_input, col_output = st.columns([1.5, 1])

with col_input:
    st.markdown("<div class='veolab-card'>", unsafe_allow_html=True)
    st.markdown("### ✍️ Input Criativo")
    
    input_type = st.radio("Selecione o tipo de entrada:", ["Texto", "Imagem", "Áudio"], horizontal=True)

    if input_type == "Texto":
        text_prompt = st.text_area("Descreva a cena ou roteiro desejado:", height=150, placeholder="Ex: Um pôr do sol vibrante sobre o oceano, com ondas suaves e um veleiro ao longe.")
    elif input_type == "Imagem":
        image_file = st.file_uploader("Upload de Imagem (base para o vídeo)", type=["png", "jpg", "jpeg"])
        image_prompt = st.text_area("Descreva a animação que deseja para a imagem:", height=100, placeholder="Ex: Animar a água com um leve movimento e o veleiro balançando.")
        
        if image_file:
            uploaded_image = Image.open(image_file)
            st.image(uploaded_image, caption="Imagem de Referência", width=200)

    elif input_type == "Áudio":
        audio_file = st.file_uploader("Upload de Áudio (Narração, Música)", type=["mp3", "wav"])
        audio_prompt = st.text_area("Descreva a cena que o áudio deve acompanhar:", height=100, placeholder="Ex: Criar um fundo visual calmo e inspirador para esta narração.")

    st.markdown("</div>", unsafe_allow_html=True)

# --- ÁREA DE GERAÇÃO E OUTPUT ---
with col_output:
    st.markdown("<div class='veolab-card'>", unsafe_allow_html=True)
    st.markdown("### 🎬 Geração e Resultado")
    
    if st.button("GERAR VÍDEO COM IA"):
        if model is None:
            st.error("O modelo Gemini não está configurado. Verifique sua API Key.")
        elif not user_email:
            st.warning("Por favor, insira seu e-mail para gerar o vídeo.")
        else:
            with st.spinner("VeoLab AI pensando... Gerando sua cena..."):
                generated_video_path = None
                
                # Exemplo SIMPLIFICADO de geração (apenas animação de texto por enquanto)
                # No futuro, aqui entraria a lógica complexa de diferentes modelos generativos
                if input_type == "Texto" and text_prompt:
                    # Geração de um vídeo básico com texto usando FFmpeg
                    generated_video_path = os.path.join(os.getcwd(), "veolab_text_gen.mp4")
                    
                    # Comando FFmpeg para criar um vídeo com texto animado
                    # Isso é um protótipo! A geração real seria muito mais complexa.
                    try:
                        cmd = [
                            'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1280x720:d=5',
                            '-vf', f"drawtext=text='{text_prompt[:50]}':x=(w-text_w)/2:y=(h-text_h)/2:fontsize=36:fontcolor=white:expansion=normal,fade=t=in:st=0:d=1,fade=t=out:st=4:d=1",
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', generated_video_path
                        ]
                        subprocess.run(cmd, check=True, capture_output=True)
                    except subprocess.CalledProcessError as e:
                        st.error(f"Erro ao gerar vídeo com FFmpeg: {e.stderr.decode()}")
                        generated_video_path = None

                if generated_video_path and os.path.exists(generated_video_path):
                    st.success("Vídeo gerado com sucesso!")
                    st.video(generated_video_path)
                    with open(generated_video_path, "rb") as f:
                        st.download_button("Baixar Vídeo (.mp4)", f, file_name="veolab_video.mp4")
                else:
                    st.error("Não foi possível gerar o vídeo. Tente novamente com outro prompt ou entrada.")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("VeoLab AI - Powered by Google Gemini. ✨")
