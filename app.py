import streamlit as st
import subprocess
import os

# --- DESIGN PREMIUM (Screenshot_18 Style) ---
st.set_page_config(page_title="ViralCut AI PRO - Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; font-family: 'Inter', sans-serif; }
    .header-gradient {
        background: linear-gradient(90deg, #4f8bf9, #ec4899);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 2.5rem; font-weight: 800; text-align: center;
    }
    .metric-card {
        background: #1a1a1a; border: 1px solid #333; 
        padding: 20px; border-radius: 12px; text-align: center;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- ACESSO PROPRIETÁRIO ---
PROPRIETARIO = "niltonrosa71@gmail.com"

with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    email = st.text_input("👤 Login", placeholder="niltonrosa71@gmail.com")
    is_admin = email.lower() == PROPRIETARIO.lower()

# --- INTERFACE PRINCIPAL ---
if email:
    st.markdown('<div class="header-gradient">ViralCut AI PRO - Dashboard</div>', unsafe_allow_html=True)
    
    # Cards Superiores
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><p>Plano</p><h3 style="color:#a855f7;">{"PRO / MASTER" if is_admin else "Gratuito"}</h3></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><p>Formato</p><h3 style="color:#6366f1;">9:16 Vertical</h3></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><p>Status</p><h3 style="color:#22c55e;">Online</h3></div>', unsafe_allow_html=True)

    st.write("---")
    col_l, col_r = st.columns([1.5, 1])

    with col_l:
        st.markdown("### 📥 Carregar Vídeo")
        video_data = st.file_uploader("", type=["mp4", "mov"])
        
    with col_r:
        st.markdown("### ⚙️ Opções")
        limite = 20 if is_admin else 1
        qtd = st.slider("Cortes", 1, limite, 1)

    if video_data:
        input_path = os.path.join(os.getcwd(), "temp_input.mp4")
        with open(input_path, "wb") as f:
            f.write(video_data.getbuffer())

        if st.button("✨ GERAR CORTES INTELIGENTES"):
            progress = st.progress(0)
            for i in range(qtd):
                saida = os.path.join(os.getcwd(), f"corte_{i+1}.mp4")
                inicio = i * 60
                
                # Comando FFmpeg Corrigido (Sem erro de aspas da Screenshot_19)
                comando = [
                    'ffmpeg', '-y', '-ss', str(inicio), '-t', '58',
                    '-i', input_path,
                    '-vf', 'crop=ih*(9/16):ih,scale=1080:1920',
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-movflags', '+faststart', saida
                ]
                
                with st.spinner(f"Renderizando parte {i+1}..."):
                    subprocess.run(comando, capture_output=True)
                
                if os.path.exists(saida):
                    st.success(f"Corte {i+1} pronto!")
                    with open(saida, "rb") as f:
                        st.download_button(f"📥 Baixar Parte {i+1}", f, file_name=f"corte_{i+1}.mp4", key=f"dl_{i}")
                
                progress.progress((i + 1) / qtd)
            st.balloons()

    # Seção de Upgrade
    st.write("---")
    st.markdown("""
        <div style="background: #1a1a1a; padding: 25px; border-radius: 12px; border-left: 5px solid #ec4899;">
            <h3>💎 Desbloqueie o potencial máximo</h3>
            <p>Gere 20 cortes simultâneos e sem marca d'água.</p>
            <button style="background:#ec4899; color:white; border:none; padding:10px 20px; border-radius:5px; font-weight:bold;">FAZER UPGRADE AGORA</button>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("Identifique-se na barra lateral para acessar o painel.")
