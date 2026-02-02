import streamlit as st
import google.generativeai as genai
import subprocess
import os

# --- CONFIGURAÇÃO DA INTERFACE HEYGEN STYLE ---
st.set_page_config(page_title="VeoLab - Video Agent IA", layout="wide", initial_sidebar_state="expanded")

# CSS para emular o design do HeyGen (Branco, minimalista e moderno)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; font-family: 'Inter', sans-serif; }
    
    /* Barra Lateral Estilo HeyGen */
    [data-testid="stSidebar"] { background-color: #f7f9fb; border-right: 1px solid #e2e8f0; }
    
    /* Botão Create (Preto arredondado) */
    .stButton>button {
        background-color: #000000; color: white; border-radius: 20px;
        padding: 10px 25px; font-weight: 600; width: 100%; border: none;
    }
    
    /* Canvas Central */
    .main-canvas {
        background: white; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 40px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    /* Estilo para Cards de Avatares */
    .avatar-card {
        border: 1px solid #edf2f7; border-radius: 8px; padding: 10px;
        text-align: center; background: #f8fafc;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONEXÃO COM A API GEMINI ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-pro')
    else:
        st.error("⚠️ Configure a API Key nos Secrets (Formato TOML).")
        model = None
except Exception as e:
    st.error(f"Erro na API: {e}")
    model = None

# --- BARRA LATERAL (ASSETS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3669/3669914.png", width=50) # Logo Simbolico
    st.markdown("### VeoLab Creator")
    st.button("➕ Create Video")
    
    st.write("---")
    st.markdown("**Assets**")
    opcao = st.radio("", ["🏠 Home", "👤 Avatars", "🖼️ Templates", "📁 Projects"])
    
    st.write("---")
    email = st.text_input("Sua Identidade", value="niltonrosa71@gmail.com")
    st.caption("Plan: Free")
    st.button("🚀 Upgrade", key="upg")

# --- CONTEÚDO PRINCIPAL (CANVAS) ---
if opcao == "🏠 Home":
    st.markdown("<h2 style='text-align: center;'>Turn your ideas into production-ready video</h2>", unsafe_allow_html=True)
    
    # Canvas de Prompt (Estilo HeyGen)
    with st.container():
        st.markdown('<div class="main-canvas">', unsafe_allow_html=True)
        
        col_av, col_txt = st.columns([1, 3])
        with col_av:
            st.markdown('<div class="avatar-card">Avatar<br><b>Auto</b></div>', unsafe_allow_html=True)
        with col_txt:
            prompt_input = st.text_area("", placeholder="Describe your video idea...", label_visibility="collapsed")
            
        st.write("")
        if st.button("✨ Generate Video", key="gen_main"):
            if not prompt_input:
                st.warning("Descreva sua ideia antes de gerar.")
            else:
                with st.spinner("VeoLab Agent is thinking..."):
                    # Processamento FFmpeg Blindado
                    output_path = "output_agent.mp4"
                    cmd = ['ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1280x720:d=5', 
                           '-vf', f"drawtext=text='{prompt_input[:30]}':fontcolor=white:x=(w-tw)/2:y=(h-th)/2", 
                           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output_path]
                    
                    try:
                        subprocess.run(cmd, check=True, capture_output=True)
                        st.video(output_path)
                        st.success("Video ready for production!")
                    except Exception as e:
                        st.error("Erro no motor de vídeo. Verifique se 'ffmpeg' está no packages.txt.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Galeria de Criações Recentes (Igual ao HeyGen)
    st.write("---")
    st.markdown("### Recent creations")
    c1, c2, c3 = st.columns(3)
    with c1: st.image("https://via.placeholder.com/300x180/f0f0f0/999999?text=Untitled+Video", caption="3 days ago")
    with c2: st.image("https://via.placeholder.com/300x180/f0f0f0/999999?text=Draft+Scene", caption="5 days ago")
    with c3: st.image("https://via.placeholder.com/300x180/f0f0f0/999999?text=Marketing+Clip", caption="1 week ago")

elif opcao == "👤 Avatars":
    st.header("Seus Avatares Digitais")
    st.info("Funcionalidade PRO: Em breve você poderá clonar sua imagem e voz.")
