import streamlit as st
import subprocess
import os
import shutil

# --- CONFIGURAÇÃO VISUAL PREMIUM (Estilo ViralCut AI) ---
st.set_page_config(page_title="ViralCut AI - Smart Video Clipping", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    .stApp { background-color: #0a0a0a; font-family: 'Inter', sans-serif; }
    .gradient-text {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 700; font-size: 3rem; text-align: center;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08); padding: 25px; border-radius: 20px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white; border: none; border-radius: 12px; font-weight: 600; width: 100%;
    }
    </style>
    <div class="gradient-text">ViralCut AI</div>
    """, unsafe_allow_html=True)

PROPRIETARIO = "niltonrosa71@gmail.com"

with st.sidebar:
    st.markdown("<h2 style='color: #a855f7;'>Configurações</h2>", unsafe_allow_html=True)
    email = st.text_input("👤 Login", placeholder="seu@email.com")

if email:
    is_admin = email.lower() == PROPRIETARIO.lower()
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f'<div class="glass-card"><p style="color: #94a3b8;">Plano</p><h3 style="color: #a855f7;">{"VIP Proprietário" if is_admin else "Gratuito"}</h3></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="glass-card"><p style="color: #94a3b8;">Formato</p><h3 style="color: #6366f1;">9:16 Vertical</h3></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="glass-card"><p style="color: #94a3b8;">Status</p><h3 style="color: #22c55e;">Online</h3></div>', unsafe_allow_html=True)

    st.write("---")
    left_col, right_col = st.columns([1.5, 1])

    with left_col:
        st.markdown("### 📥 Carregar Vídeo")
        video_file = st.file_uploader("", type=["mp4", "mov", "mpeg"])
        
    with right_col:
        st.markdown("### ⚙️ Opções")
        limite = st.slider("Quantidade de cortes", 1, 15, (10 if is_admin else 1))

    if video_file:
        # Caminho absoluto para evitar FileNotFoundError
        input_path = os.path.join(os.getcwd(), "input_video.mp4")
        with open(input_path, "wb") as f:
            f.write(video_file.getbuffer())

        if st.button("✨ GERAR CORTES INTELIGENTES"):
            progress_bar = st.progress(0)
            
            for i in range(limite):
                inicio = i * 60
                saida = os.path.join(os.getcwd(), f"corte_viral_{i+1}.mp4")
                
                # Comando otimizado para servidores Linux (Streamlit Cloud)
                comando = [
                    'ffmpeg', '-y', '-ss', str(inicio), '-t', '58', 
                    '-i', input_path, 
                    '-vf', 'crop=ih*(9/16):ih,scale=1080:1920', 
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', 
                    '-c:a', 'aac', '-movflags', '+faststart', saida
                ]
                
                try:
                    subprocess.run(comando, check=True, capture_output=True)
                    progress_bar.progress((i + 1) / limite)
                    
                    if os.path.exists(saida):
                        with st.expander(f"✅ Corte #{i+1} pronto"):
                            with open(saida, "rb") as f:
                                st.download_button(f"Baixar MP4 Parte {i+1}", f, file_name=f"corte_{i+1}.mp4", key=f"btn_{i}")
                except Exception as e:
                    st.error(f"Erro no corte {i+1}. O vídeo original pode ser curto demais.")
            
            st.balloons()
else:
    st.info("Por favor, faça login para acessar o painel.")
