import streamlit as st
import google.generativeai as genai
import subprocess
import os

# --- INTERFACE VEO 3 PREMIUM ---
st.set_page_config(page_title="ViralCut AI - Veo Multimedia Studio", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    .veo-card { background: #0f0f0f; border: 1px solid #1f1f1f; padding: 25px; border-radius: 4px; }
    .main-title { font-weight: 300; font-size: 2.5rem; color: #ffffff; letter-spacing: -1px; text-align: center; }
    .stButton>button { background-color: #ffffff; color: #000; border-radius: 2px; font-weight: 600; width: 100%; height: 3.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE ACESSO VIP ---
PROPRIETARIO = "niltonrosa71@gmail.com"

with st.sidebar:
    st.markdown("### VIRALCUT **VEO**")
    email = st.text_input("Identidade", placeholder="seu@email.com")
    is_admin = (email.lower() == PROPRIETARIO.lower()) if email else False

if email:
    st.markdown("<div class='main-title'>Laboratório de Criação Multimídia</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🎥 Vídeo para Cortes", "🖼️ Imagem para Vídeo", "🎙️ Texto/Áudio para Vídeo"])

    with tab1:
        st.markdown("### Transformação de Vídeos Longos")
        v_file = st.file_uploader("Upload MP4/MOV", type=["mp4", "mov"])
        if v_file and st.button("GERAR CORTES VIRAIS"):
            # Lógica blindada de processamento
            input_p = os.path.join(os.getcwd(), "input.mp4")
            with open(input_p, "wb") as f: f.write(v_file.getbuffer())
            
            output_p = os.path.join(os.getcwd(), "output_veo.mp4")
            # Marca d'água automática para divulgação gratuita
            filtro = "crop=ih*(9/16):ih,scale=1080:1920" if is_admin else "crop=ih*(9/16):ih,scale=1080:1920,drawtext=text='ViralCut AI':x=w-tw-20:y=h-th-20:fontsize=30:fontcolor=white@0.5"
            
            cmd = ['ffmpeg', '-y', '-i', input_p, '-t', '58', '-vf', filtro, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output_p]
            subprocess.run(cmd, capture_output=True)
            
            if os.path.exists(output_p):
                st.success("Processamento concluído com sucesso!")
                with open(output_p, "rb") as f:
                    st.download_button("📥 Baixar Resultado", f, file_name="corte_veo.mp4")

    with tab2:
        st.markdown("### Estilo Veo: Imagem Animada")
        st.info("Utilize imagens para criar cenas dinâmicas.")
        i_file = st.file_uploader("Upload Foto", type=["jpg", "png"])
        prompt = st.text_area("Descreva o movimento da cena...")
        if st.button("ANIMAR COM IA"):
            st.warning("Integração com API de geração de vídeo em processamento.")

else:
    st.info("Autentique-se na barra lateral para acessar o estúdio.")
