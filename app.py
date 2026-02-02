import streamlit as st
import subprocess
import os
import time

# --- SETUP DA PÁGINA ---
st.set_page_config(page_title="ViralCut AI - Smart Video Clipping", layout="wide", initial_sidebar_state="expanded")

# --- DESIGN PREMIUM ESTILO REKA / DARK MODE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp { background-color: #0d0d0d; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Dashboard Cards */
    .dashboard-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        text-align: left;
    }
    
    /* Títulos em Gradiente */
    .title-gradient {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 2.5rem; font-weight: 800;
    }

    /* Botão Estilizado */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white; border: none; border-radius: 10px;
        padding: 12px; font-weight: 600; width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(168, 85, 247, 0.3); }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE ACESSO ---
PROPRIETARIO = "niltonrosa71@gmail.com"
if 'creditos_usados' not in st.session_state:
    st.session_state['creditos_usados'] = 0

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #a855f7;'>ViralCut AI</h2>", unsafe_allow_html=True)
    user_email = st.text_input("👤 Login do Usuário", placeholder="ex@email.com")
    st.write("---")
    st.markdown("### 💎 Plano PRO")
    st.write("Cortes ilimitados e sem marca d'água.")
    st.button("Fazer Upgrade (R$ 49,90/mês)")

# --- DASHBOARD ---
if user_email:
    is_admin = user_email.lower() == PROPRIETARIO.lower()
    
    # Header do Proprietário ou Usuário
    if is_admin:
        st.markdown("<div class='title-gradient'>Painel do Proprietário</div>", unsafe_allow_html=True)
        st.success(f"👑 Bem-vindo, Nilton! Seu acesso é ilimitado.")
        creditos = "∞"
        limite_cortes = 15
    else:
        st.markdown("<div class='title-gradient'>Seu Estúdio IA</div>", unsafe_allow_html=True)
        creditos = max(0, 2 - st.session_state['creditos_usados'])
        limite_cortes = 1
        if creditos == 0:
            st.error("Seus créditos acabaram. Torne-se PRO para continuar.")

    # Linha de Informações (Cartões Visuais)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='dashboard-card'><small>Status do Plano</small><h3>{'👑 PRO' if is_admin else 'Gratuito'}</h3></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='dashboard-card'><small>Créditos Restantes</small><h3>{creditos}</h3></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='dashboard-card'><small>Formato de Saída</small><h3>9:16 Vertical</h3></div>", unsafe_allow_html=True)

    st.write("---")

    # Área de Trabalho
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.markdown("### 🎥 Carregar Original")
        video_file = st.file_uploader("", type=["mp4", "mov"])
        
    with col_r:
        st.markdown("### ⚙️ Ajustes")
        qtd = st.slider("Cortes desejados", 1, limite_cortes, (5 if is_admin else 1))

    if video_file and (is_admin or creditos > 0):
        input_path = "video_temp.mp4"
        with open(input_path, "wb") as f:
            f.write(video_file.getbuffer())

        if st.button("✨ GERAR CORTES VIRAIS AGORA"):
            st.write("---")
            progresso = st.progress(0)
            
            # CRIAR ÁREA DE RESULTADOS DINÂMICA
            container_downloads = st.container()
            
            for i in range(qtd):
                inicio = i * 60
                saida = f"corte_viral_{i+1}.mp4"
                
                # Comando FFmpeg corrigido (indentações e metadados)
                comando = f'ffmpeg -y -ss {inicio} -t 58 -i {input_path} -vf "crop=ih*(9/16):ih,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart {saida}'
                
                with st.spinner(f"Processando corte {i+1}..."):
                    subprocess.run(comando, shell=True)
                
                progresso.progress((i + 1) / qtd)
                
                # RESOLUÇÃO DO ERRO: Mostrar download imediatamente após criar cada arquivo
                with container_downloads:
                    if os.path.exists(saida):
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.info(f"✅ Corte #{i+1} pronto para download!")
                        with col_b:
                            with open(saida, "rb") as f:
                                st.download_button(f"Baixar Parte {i+1}", f, file_name=saida, key=f"btn_{i}")
            
            if not is_admin:
                st.session_state['creditos_usados'] += 1
            st.balloons()
else:
    st.markdown("<div style='text-align: center; padding-top: 100px;'><h2>Aguardando login na barra lateral...</h2></div>", unsafe_allow_html=True)
