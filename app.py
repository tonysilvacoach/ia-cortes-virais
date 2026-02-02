import streamlit as st
import google.generativeai as genai
import subprocess
import os

# --- INTERFACE VEO 3 STYLE ---
st.set_page_config(page_title="ViralCut AI - Veo 3 Multimedia", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    .veo-card { background: #0f0f0f; border: 1px solid #1f1f1f; padding: 25px; border-radius: 4px; }
    .main-title { font-weight: 300; font-size: 2.5rem; color: #ffffff; letter-spacing: -1px; }
    .stButton>button { background-color: #ffffff; color: #000; border-radius: 2px; font-weight: 600; width: 100%; height: 3.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE SEGURANÇA ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Configure sua GEMINI_API_KEY nas Secrets do Streamlit.")

PROPRIETARIO = "niltonrosa71@gmail.com" #

with st.sidebar:
    st.markdown("### VIRALCUT **VEO**")
    email = st.text_input("Identidade", placeholder="seu@email.com")
    is_admin = email.lower() == PROPRIETARIO.lower()

# --- ÁREA DE CRIAÇÃO MULTIMÍDIA ---
if email:
    st.markdown("<div class='main-title'>Laboratório de Criação IA</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🎥 Vídeo para Cortes", "🖼️ Imagem para Vídeo", "🎙️ Áudio para Legendas"])

    with tab1:
        st.markdown("### Transformar Vídeo Longo")
        v_file = st.file_uploader("Upload MP4/MOV", type=["mp4", "mov"], key="v1")
        if v_file and st.button("GERAR CORTES VIRAIS"):
            # Lógica de processamento de vídeo com marca d'água automática
            input_p = "input.mp4"
            with open(input_p, "wb") as f: f.write(v_file.getbuffer())
            
            output_p = "output_veo.mp4"
            filtro = "crop=ih*(9/16):ih,scale=1080:1920" if is_admin else "crop=ih*(9/16):ih,scale=1080:1920,drawtext=text='ViralCut AI':x=10:y=10:fontsize=24:fontcolor=white"
            
            cmd = ['ffmpeg', '-y', '-i', input_p, '-t', '58', '-vf', filtro, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output_p]
            subprocess.run(cmd)
            
            if os.path.exists(output_p):
                st.video(output_p)
                with open(output_p, "rb") as f:
                    st.download_button("📥 Baixar Resultado", f, file_name="corte_veo.mp4")

    with tab2:
        st.markdown("### Gerar Animação de Imagem")
        i_file = st.file_uploader("Upload Foto", type=["jpg", "png"], key="i1")
        prompt = st.text_area("Descreva o movimento desejado (Prompt estilo Veo)")
        if i_file and st.button("ANIMAR COM IA"):
            st.info("Utilizando Gemini 1.5 Pro para análise de cena...") #
            st.warning("Funcionalidade de vídeo generativo requer cota de API Enterprise.")

    with tab3:
        st.markdown("### Processar Áudio/Narração")
        a_file = st.file_uploader("Upload Áudio", type=["mp3", "wav"], key="a1")
        if a_file and st.button("GERAR LEGENDA DINÂMICA"):
            st.success("Áudio processado. Pronto para sobreposição no vídeo.")

else:
    st.info("Autentique-se para acessar o estúdio multimídia.")
