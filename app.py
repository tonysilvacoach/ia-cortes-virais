import streamlit as st
import subprocess
import os
import time

# --- DESIGN PREMIUM REKA STYLE ---
st.set_page_config(page_title="ViralCut PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #fafafa; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1a1a1a; }
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 15px; margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white; border: none; border-radius: 10px; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- ACESSO VIP ---
PROPRIETARIO = "niltonrosa71@gmail.com"

with st.sidebar:
    st.markdown("<h1 style='color: #a855f7;'>ViralCut AI</h1>", unsafe_allow_html=True)
    email = st.text_input("👤 Login", placeholder="niltonrosa71@gmail.com")
    st.write("---")
    st.markdown("### Status do Plano")
    if email.lower() == PROPRIETARIO.lower():
        st.success("👑 Proprietário VIP")
        limite = 20
    else:
        st.info("Plano Gratuito")
        limite = 1

# --- DASHBOARD ---
if email:
    st.markdown(f"## Bem-vindo ao Estúdio, {email.split('@')[0]}!")
    
    col_u, col_s = st.columns([1.5, 1])
    
    with col_u:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📥 1. Upload do Vídeo")
        video = st.file_uploader("", type=["mp4", "mov", "mpeg"])
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_s:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ 2. Inteligência")
        qtd = st.slider("Quantidade de cortes", 1, limite, 1)
        st.caption(f"Capacidade atual: {limite} cortes.")
        st.markdown('</div>', unsafe_allow_html=True)

    if video:
        with open("base_video.mp4", "wb") as f:
            f.write(video.getbuffer())

        if st.button("🚀 GERAR CORTES VIRAIS"):
            progress = st.progress(0)
            status = st.empty()
            
            for i in range(qtd):
                saida = f"corte_{i+1}.mp4"
                inicio = i * 60
                status.markdown(f"🤖 **Processando Parte {i+1}...**")
                
                # Comando FFmpeg otimizado
                cmd = f'ffmpeg -y -ss {inicio} -t 58 -i base_video.mp4 -vf "crop=ih*(9/16):ih,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart {saida}'
                
                process = subprocess.run(cmd, shell=True, capture_output=True)
                
                if process.returncode == 0 and os.path.exists(saida):
                    st.markdown(f'### ✅ Corte #{i+1} Pronto')
                    with open(saida, "rb") as f:
                        st.download_button(f"📥 Baixar Corte {i+1}", f, file_name=saida, key=f"dl_{i}")
                else:
                    st.error(f"Erro ao gerar o corte {i+1}. Verifique a duração do vídeo.")
                
                progress.progress((i + 1) / qtd)
            st.balloons()
else:
    st.warning("Aguardando login na barra lateral...")
