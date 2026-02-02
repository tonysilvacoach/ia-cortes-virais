import streamlit as st
import subprocess
import os

# --- CONFIGURAÇÃO VISUAL PREMIUM (Estilo Dashboard enviado) ---
st.set_page_config(page_title="ViralCut AI PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #0d0d0d; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    .main-title { background: linear-gradient(90deg, #4f8bf9, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; font-weight: 800; text-align: center; }
    
    .dashboard-card { background: #1a1a1a; border: 1px solid #333; padding: 20px; border-radius: 12px; text-align: center; height: 100%; }
    
    .stButton>button { background: linear-gradient(90deg, #6366f1, #a855f7); color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%; height: 3.5rem; }
    
    .upgrade-section { background: #1e1e1e; padding: 25px; border-radius: 15px; border-left: 5px solid #ec4899; margin-top: 30px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN E SEGURANÇA ---
PROPRIETARIO = "niltonrosa71@gmail.com"

with st.sidebar:
    st.markdown("<h2 style='color: #a855f7;'>Configurações</h2>", unsafe_allow_html=True)
    user_email = st.text_input("👤 E-mail de Login", placeholder="seu@email.com")
    st.write("---")
    is_admin = user_email.lower() == PROPRIETARIO.lower() if user_email else False

# --- INTERFACE PRINCIPAL ---
if user_email:
    st.markdown('<div class="main-title">ViralCut AI PRO - Dashboard</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>Transforme vídeos longos em conteúdo viral com IA</p>", unsafe_allow_html=True)

    # Cards de Status (Igual à imagem)
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f'<div class="dashboard-card"><p>Plano</p><h3 style="color:#a855f7;">{"PRO / MASTER" if is_admin else "Gratuito"}</h3></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="dashboard-card"><p>Formato</p><h3 style="color:#6366f1;">9:16 Vertical</h3></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="dashboard-card"><p>Status</p><h3 style="color:#22c55e;">Online</h3></div>', unsafe_allow_html=True)

    st.write("---")
    
    left_c, right_c = st.columns([1.5, 1])
    with left_c:
        st.markdown("### 📥 Carregar Vídeo")
        video_up = st.file_uploader("", type=["mp4", "mov", "mpeg"])
    with right_c:
        st.markdown("### ⚙️ Opções")
        limite = 20 if is_admin else 1
        qtd = st.slider("Quantidade de cortes", 1, limite, 1)

    if video_up:
        input_path = os.path.join(os.getcwd(), "video_input.mp4")
        with open(input_path, "wb") as f: f.write(video_up.getbuffer())

        if st.button("✨ GERAR CORTES INTELIGENTES"):
            progresso = st.progress(0)
            for i in range(qtd):
                saida = os.path.join(os.getcwd(), f"corte_{i+1}.mp4")
                inicio = i * 60
                
                # COMANDO CORRIGIDO (SEM ERROS DE ASPAS)
                comando = [
                    'ffmpeg', '-y', '-ss', str(inicio), '-t', '58',
                    '-i', input_path,
                    '-vf', 'crop=ih*(9/16):ih,scale=1080:1920',
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-movflags', '+faststart', saida
                ]
                
                with st.spinner(f"Processando corte {i+1}..."):
                    subprocess.run(comando, capture_output=True)
                
                if os.path.exists(saida):
                    st.success(f"✅ Corte {i+1} finalizado!")
                    with open(saida, "rb") as f:
                        st.download_button(f"Baixar Corte {i+1}", f, file_name=f"corte_{i+1}.mp4", key=f"dl_{i}")
                
                progresso.progress((i + 1) / qtd)
            st.balloons()

    # Seção Upgrade (Igual à imagem)
    st.markdown("""
        <div class="upgrade-section">
            <h2 style="color: #ec4899;">💎 Desbloqueie todo o potencial AI</h2>
            <p style="color: #94a3b8;">Gere 20 cortes de uma vez e com prioridade na renderização.</p>
            <br>
            <button style="background:#ec4899; color:white; border:none; padding:15px 40px; border-radius:10px; font-weight:bold; cursor:pointer;">FAZER UPGRADE AGORA (R$ 49,90)</button>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("Por favor, faça login na barra lateral para acessar o sistema.")
