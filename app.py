import streamlit as st
import subprocess
import os

# --- ESTILO VIRALCUT AI (DARK MODE PROFISSIONAL) ---
st.set_page_config(page_title="ViralCut Pro - Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 25px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        border: none; border-radius: 15px; color: white; font-weight: bold;
    }
    .sidebar .sidebar-content { background-color: #0a0a0a; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES DE ACESSO ---
PROPRIETARIO = "niltonrosa71@gmail.com"

with st.sidebar:
    st.markdown("<h1 style='color: #6366f1;'>VIRAL<span style='color:white'>LAB</span></h1>", unsafe_allow_html=True)
    st.write("---")
    email = st.text_input("🔑 Login de Acesso", placeholder="seu@email.com")

if email:
    is_admin = email.lower() == PROPRIETARIO.lower()
    
    # Header Estilo SaaS
    st.markdown(f"## Video <span style='color:#a855f7'>Power Studio</span>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        upload = st.file_uploader("Upload do Vídeo Original", type=["mp4", "mov"])
        if is_admin:
            st.success("👑 Acesso Ilimitado Nilton Rosa")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("📈 **Status da Conta**")
        st.write(f"Plano: {'PRO Ilimitado' if is_admin else 'Gratuito'}")
        num_cortes = 15 if is_admin else 1
        st.markdown("</div>", unsafe_allow_html=True)

    if upload:
        with open("temp.mp4", "wb") as f:
            f.write(upload.getbuffer())
        
        if st.button("🚀 INICIAR INTELIGÊNCIA DE CORTE"):
            for i in range(num_cortes):
                saida = f"corte_{i+1}.mp4"
                # Motor FFmpeg profissional corrigido
                comando = f'ffmpeg -y -ss {i*60} -t 59 -i temp.mp4 -vf "crop=ih*(9/16):ih,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart {saida}'
                subprocess.run(comando, shell=True)
                
                with st.expander(f"✅ Corte {i+1} Finalizado"):
                    with open(saida, "rb") as f:
                        st.download_button(f"Download MP4", f, file_name=saida)
else:
    st.warning("⚠️ Identifique-se para acessar o Power Studio.")
