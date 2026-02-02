import streamlit as st
import subprocess
import os
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ViralCut AI PRO - Dashboard", layout="wide")

# --- CSS PARA INTERFACE DA FOTO (MODERNA E DARK) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp { background-color: #0d0d0d; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Header e Títulos */
    .main-title { background: linear-gradient(90deg, #4f8bf9, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; font-weight: 800; text-align: center; }
    .sub-title { text-align: center; color: #94a3b8; margin-bottom: 2rem; }

    /* Cards Estilo Foto */
    .dashboard-card { background: #1a1a1a; border: 1px solid #333; padding: 20px; border-radius: 12px; text-align: center; }
    .status-online { color: #22c55e; font-weight: bold; }
    
    /* Botões */
    .stButton>button { background: linear-gradient(90deg, #6366f1, #a855f7); color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%; height: 3rem; }
    .upgrade-btn { background: #ec4899 !important; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #222; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE ACESSO ---
PROPRIETARIO = "niltonrosa71@gmail.com"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    email = st.text_input("👤 E-mail de Login", placeholder="niltonrosa71@gmail.com")
    st.write("---")
    if email.lower() == PROPRIETARIO.lower():
        st.success("👑 Proprietário VIP")
        limite_cortes = 20
    else:
        st.info("Plano Gratuito")
        limite_cortes = 1

# --- CONTEÚDO PRINCIPAL ---
st.markdown('<div class="main-title">ViralCut AI PRO - Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Transforme vídeos longos em conteúdo viral com IA.</div>', unsafe_allow_html=True)

# Linha Superior (Cards da Foto)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="dashboard-card"><p>Plano</p><h3 style="color:#a855f7;">{"PRO / MASTER" if email.lower() == PROPRIETARIO.lower() else "Gratuito"}</h3></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="dashboard-card"><p>Formato</p><h3 style="color:#6366f1;">9:16 Vertical</h3><span class="status-online">Ativo</span></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="dashboard-card"><p>Status</p><h3 style="color:#22c55e;">Online</h3><p>IA Pronta</p></div>', unsafe_allow_html=True)

st.write("---")

# Área de Trabalho (Upload e Opções)
col_l, col_r = st.columns([1.5, 1])

with col_l:
    st.markdown("### 📥 Carregar Vídeo")
    video_data = st.file_uploader("", type=["mp4", "mov", "mpeg"])

with col_r:
    st.markdown("### ⚙️ Opções")
    qtd_cortes = st.slider("Quantidade de cortes", 1, limite_cortes, (10 if email.lower() == PROPRIETARIO.lower() else 1))
    if st.button("✨ GERAR CORTES INTELIGENTES"):
        if video_data:
            input_path = "temp_video.mp4"
            with open(input_path, "wb") as f:
                f.write(video_data.getbuffer())
            
            # Container de Resultados
            st.write("---")
            progresso = st.progress(0)
            
            for i in range(qtd_cortes):
                saida = f"corte_viral_{i+1}.mp4"
                inicio = i * 60
                
                # Motor FFmpeg Blindado
                comando = f'ffmpeg -y -ss {inicio} -t 58 -i {input_path} -vf "crop=ih*(9/16):ih,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart {saida}'
                
                with st.spinner(f"Processando parte {i+1}..."):
                    res = subprocess.run(comando, shell=True, capture_output=True)
                
                if os.path.exists(saida):
                    st.success(f"✅ Corte #{i+1} finalizado!")
                    with open(saida, "rb") as f:
                        st.download_button(f"📥 Baixar Corte {i+1}", f, file_name=saida, key=f"btn_{i}")
                else:
                    st.error(f"Erro no corte {i+1}. O vídeo pode ser curto demais.")
                
                progresso.progress((i + 1) / qtd_cortes)
            st.balloons()
        else:
            st.warning("Por favor, suba um vídeo primeiro.")

# Card de Upgrade (Igual à Foto)
st.write("---")
st.markdown("""
    <div style="background: #1e1e1e; padding: 25px; border-radius: 15px; border-left: 5px solid #ec4899;">
        <h3>💎 Desbloqueie todo o potencial da IA</h3>
        <p>Gere 10x mais cortes, sem marca d'água e com prioridade.</p>
    </div>
""", unsafe_allow_html=True)
if st.button("🚀 FAZER UPGRADE AGORA (R$ 49,90)", key="upgrade"):
    st.info("Redirecionando para o Checkout...")
