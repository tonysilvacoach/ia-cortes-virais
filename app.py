import streamlit as st
import subprocess
import os

# --- INTERFACE PREMIUM ---
st.set_page_config(page_title="ViralCut AI PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .dashboard-card { background: #111; border: 1px solid #222; padding: 20px; border-radius: 12px; text-align: center; }
    .stButton>button { background: linear-gradient(90deg, #6366f1, #a855f7); color: white; border: none; border-radius: 8px; width: 100%; height: 3rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN ---
PROPRIETARIO = "niltonrosa71@gmail.com" #

with st.sidebar:
    st.title("ViralCut AI")
    email = st.text_input("👤 Login", placeholder="seu@email.com")
    is_admin = email.lower() == PROPRIETARIO.lower() if email else False

# --- DASHBOARD ---
if email:
    st.markdown(f"## Dashboard: {'Proprietário VIP' if is_admin else 'Usuário'}") #
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="dashboard-card"><p>Plano</p><h3>{"PRO" if is_admin else "FREE"}</h3></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="dashboard-card"><p>Formato</p><h3>9:16 Vertical</h3></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="dashboard-card"><p>Motor</p><h3 style="color:#22c55e;">Ativo</h3></div>', unsafe_allow_html=True)

    st.write("---")
    video_file = st.file_uploader("Suba seu vídeo aqui", type=["mp4", "mov"])

    if video_file:
        if st.button("✨ GERAR CORTE"):
            input_path = "video_teste.mp4"
            with open(input_path, "wb") as f:
                f.write(video_file.getbuffer())
            
            saida = "resultado.mp4"
            # Comando direto para evitar erro de sintaxe
            comando = f'ffmpeg -y -i {input_path} -t 10 -vf "crop=ih*(9/16):ih,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p {saida}'
            
            with st.spinner("IA Processando..."):
                subprocess.run(comando, shell=True)
            
            if os.path.exists(saida):
                st.success("Corte finalizado!")
                with open(saida, "rb") as f:
                    st.download_button("📥 Baixar Vídeo", f, file_name=saida)
else:
    st.info("Aguardando login...")
