import streamlit as st
import subprocess
import os

# --- DESIGN CINEMATIC VEO 3 ---
st.set_page_config(page_title="ViralCut AI - Powered by Veo Engine", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    /* Estética Dark Gray Veo */
    .stApp {
        background-color: #050505;
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }
    
    /* Cards de Interface */
    .veo-card {
        background: #0f0f0f;
        border: 1px solid #1f1f1f;
        padding: 30px;
        border-radius: 4px; /* Veo usa bordas mais retas e elegantes */
    }
    
    /* Título Minimalista */
    .veo-header {
        letter-spacing: -1px;
        font-weight: 300;
        font-size: 2.2rem;
        color: #ffffff;
        margin-bottom: 2rem;
    }

    /* Botão Veo (Branco com Hover Suave) */
    .stButton>button {
        background-color: #ffffff;
        color: #000000;
        border-radius: 2px;
        font-weight: 600;
        border: none;
        height: 3rem;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background-color: #cccccc;
    }

    /* Sidebar Veo */
    [data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid #111111;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE ACESSO ---
PROPRIETARIO = "niltonrosa71@gmail.com"

with st.sidebar:
    st.markdown("<h3 style='font-weight:300;'>VIRALCUT <span style='font-weight:600;'>PRO</span></h3>", unsafe_allow_html=True)
    user_email = st.text_input("Identidade", placeholder="email@exemplo.com")
    st.write("---")
    st.caption("Veo Engine v3.0 | Status: Ativo")

# --- ÁREA DE CRIAÇÃO ---
if user_email:
    is_admin = user_email.lower() == PROPRIETARIO.lower()
    
    st.markdown("<div class='veo-header'>Criar conteúdo viral</div>", unsafe_allow_html=True)
    
    # Grid de Ferramentas
    col_main, col_tools = st.columns([2, 1])
    
    with col_main:
        st.markdown("#### 1. Mídia de Origem")
        video_input = st.file_uploader("", type=["mp4", "mov", "mpeg"])
        
    with col_tools:
        st.markdown("#### 2. Parâmetros")
        num_cortes = st.select_slider("Capacidade de geração", options=[1, 5, 10, 15, 20], value=(20 if is_admin else 1))
        st.write(f"Modo: {'💎 Proprietário' if is_admin else '✨ Gratuito (com marca)'}")

    if video_input:
        video_path = os.path.join(os.getcwd(), "source_video.mp4")
        with open(video_path, "wb") as f:
            f.write(video_input.getbuffer())

        if st.button("GERAR VÍDEOS"):
            progress = st.progress(0)
            
            for i in range(num_cortes):
                saida_nome = f"corte_veo_{i+1}.mp4"
                saida_path = os.path.join(os.getcwd(), saida_nome)
                inicio = i * 60

                # Lógica de Marca d'água (Marketing Orgânico)
                if is_admin:
                    filtro = "crop=ih*(9/16):ih,scale=1080:1920"
                else:
                    filtro = "crop=ih*(9/16):ih,scale=1080:1920,drawtext=text='ViralCut AI':x=w-tw-20:y=h-th-20:fontsize=30:fontcolor=white@0.5"

                # Comando FFmpeg de Alta Performance
                comando = [
                    'ffmpeg', '-y', '-ss', str(inicio), '-t', '58',
                    '-i', video_path,
                    '-vf', filtro,
                    '-c:v', libx264', '-preset', 'faster', '-crf', '21',
                    '-c:a', 'aac', '-movflags', '+faststart', saida_path
                ]
                
                with st.spinner(f"Renderizando sequência {i+1}..."):
                    subprocess.run(comando, capture_output=True)
                
                if os.path.exists(saida_path):
                    st.success(f"Sequência {i+1} finalizada")
                    with open(saida_path, "rb") as f:
                        st.download_button(f"Baixar MP4 - v{i+1}", f, file_name=saida_nome, key=f"v_{i}")
                
                progress.progress((i + 1) / num_cortes)
            
            st.balloons()
else:
    st.markdown("<div style='text-align: center; margin-top: 150px; opacity: 0.5;'>Autentique sua conta para acessar o estúdio.</div>", unsafe_allow_html=True)
