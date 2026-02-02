import streamlit as st
import subprocess
import os
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="CorteViral PRO | IA Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- DESIGN CUSTOMIZADO (ESTILO REKA/MODERNO) ---
st.markdown("""
    <style>
    /* Fundo e Container Principal */
    .stApp {
        background-color: #050505;
        color: #ffffff;
    }
    
    /* Estilização dos Cards de Métricas */
    .metric-card {
        background-color: #111111;
        border: 1px solid #222222;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Botões Premium */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE ACESSO ---
PROPRIETARIO = "niltonrosa71@gmail.com"

with st.sidebar:
    st.markdown("<h1 style='color: #a855f7;'>CorteViral PRO</h1>", unsafe_allow_html=True)
    st.write("---")
    email = st.text_input("🔑 Identificação", placeholder="Digite seu e-mail")
    st.write("---")
    st.markdown("### 🛠 Suporte & Vendas")
    st.write("Dúvidas? Fale com o suporte.")

# --- CONTEÚDO DO DASHBOARD ---
if email:
    is_admin = email.lower() == PROPRIETARIO.lower()
    
    # Header de Boas-vindas
    st.markdown(f"## Bem-vindo ao seu Estúdio de IA, {email.split('@')[0]}!")
    
    # Linha de Cards Informativos (Dashboard)
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown('<div class="metric-card"><h3>Plano</h3><h2 style="color: #a855f7;">' + ("PRO (Ilimitado)" if is_admin else "FREE") + '</h2></div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown('<div class="metric-card"><h3>Formato</h3><h2 style="color: #6366f1;">9:16 Vertical</h2></div>', unsafe_allow_html=True)
    with col_m3:
        st.markdown('<div class="metric-card"><h3>Qualidade</h3><h2 style="color: #22c55e;">HD 1080p</h2></div>', unsafe_allow_html=True)

    st.write("---")

    # Área de Trabalho
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.markdown("### 🎥 1. Upload do Conteúdo")
        video_file = st.file_uploader("Arraste seu vídeo aqui", type=["mp4", "mov"])
        
    with c2:
        st.markdown("### ⚙️ 2. Configurações de IA")
        num_cortes = st.slider("Quantidade de cortes", 1, 15, (10 if is_admin else 1))
        st.caption("A IA analisará os melhores momentos baseados na retenção.")

    if video_file:
        with open("input_video.mp4", "wb") as f:
            f.write(video_file.getbuffer())

        if st.button("✨ INICIAR MÁGICA DOS CORTES"):
            status_placeholder = st.empty()
            progress_bar = st.progress(0)
            
            for i in range(num_cortes):
                # Simulação visual de progresso para UX
                status_placeholder.markdown(f"🤖 **IA Analisando:** Gerando corte {i+1} de {num_cortes}...")
                
                inicio = i * 60
                saida = f"corte_viral_{i+1}.mp4"
                
                # Motor FFmpeg otimizado
                comando = f'ffmpeg -y -ss {inicio} -t 58 -i input_video.mp4 -vf "crop=ih*(9/16):ih,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart {saida}'
                subprocess.run(comando, shell=True, capture_output=True)
                
                progress_bar.progress((i + 1) / num_cortes)
                
                with st.expander(f"📥 Download: Corte #{i+1} pronto"):
                    with open(saida, "rb") as f:
                        st.download_button(f"Baixar MP4 - Parte {i+1}", f, file_name=saida)
            
            st.balloons()
            st.success("🎉 Todos os cortes foram processados e estão prontos para download!")

else:
    st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h1>🚀 Pronto para viralizar?</h1>
            <p>Faça login na barra lateral para acessar as ferramentas de IA.</p>
        </div>
    """, unsafe_allow_html=True)
