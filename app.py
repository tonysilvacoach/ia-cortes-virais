import streamlit as st
import subprocess
import os

# --- DESIGN PREMIUM VIRALCUT ---
st.set_page_config(page_title="ViralCut AI PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #080808; color: #ffffff; }
    .metric-card {
        background: #111; border: 1px solid #222; 
        padding: 20px; border-radius: 15px; text-align: center;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: white; border-radius: 10px; font-weight: bold; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- ACESSO PROPRIETÁRIO ---
PROPRIETARIO = "niltonrosa71@gmail.com"

with st.sidebar:
    st.title("ViralCut AI")
    email = st.text_input("👤 Login", placeholder="niltonrosa71@gmail.com")
    is_admin = email.lower() == PROPRIETARIO.lower()

# --- DASHBOARD ---
if email:
    st.markdown(f"## Dashboard de {'Proprietário' if is_admin else 'Usuário'}")
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f'<div class="metric-card"><p>Plano</p><h3>{"PRO" if is_admin else "FREE"}</h3></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="metric-card"><p>Formato</p><h3>9:16 Vertical</h3></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="metric-card"><p>Status</p><h3 style="color:#22c55e;">Online</h3></div>', unsafe_allow_html=True)

    st.write("---")
    
    c1, c2 = st.columns([1.5, 1])
    with c1:
        video_upload = st.file_uploader("📥 Arraste seu vídeo", type=["mp4", "mov"])
    with c2:
        qtd = st.slider("Cortes", 1, 15, (10 if is_admin else 1))

    if video_upload:
        # Caminho absoluto para evitar erros de File Not Found
        current_dir = os.path.dirname(os.path.abspath(__file__))
        video_path = os.path.join(current_dir, "input.mp4")
        
        with open(video_path, "wb") as f:
            f.write(video_upload.getbuffer())

        if st.button("🚀 INICIAR EDIÇÃO"):
            for i in range(qtd):
                saida_nome = f"corte_{i+1}.mp4"
                saida_path = os.path.join(current_dir, saida_nome)
                inicio = i * 60
                
                # Comando FFmpeg otimizado para o servidor
                comando = [
                    'ffmpeg', '-y', '-ss', str(inicio), '-t', '58', 
                    '-i', video_path, 
                    '-vf', 'crop=ih*(9/16):ih,scale=1080:1920', 
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-movflags', '+faststart', saida_path
                ]
                
                with st.spinner(f"Processando corte {i+1}..."):
                    subprocess.run(comando, capture_output=True)
                
                if os.path.exists(saida_path):
                    st.success(f"Corte {i+1} finalizado!")
                    with open(saida_path, "rb") as f:
                        st.download_button(f"📥 Baixar Corte {i+1}", f, file_name=saida_nome, key=f"dl_{i}")
            st.balloons()
else:
    st.warning("Por favor, faça login na barra lateral.")
