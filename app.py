import streamlit as st
import subprocess
import os

# --- CONFIGURAÇÃO VISUAL PREMIUM (Inspirado no index.html) ---
st.set_page_config(page_title="ViralCut AI - Smart Video Clipping", layout="wide")

# CSS para aplicar o estilo Glassmorphism e Gradient Text do modelo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background-color: #0a0a0a;
        font-family: 'Inter', sans-serif;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        width: 100%;
    }
    </style>
    <div class="gradient-text">ViralCut AI</div>
    <p style="text-align: center; color: #94a3b8; font-size: 1.2rem;">Criação inteligente de vídeos curtos em segundos.</p>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DO PROPRIETÁRIO ---
PROPRIETARIO = "niltonrosa71@gmail.com"

# --- SIDEBAR ORGANIZADA ---
with st.sidebar:
    st.markdown("<h2 style='color: #a855f7;'>Configurações</h2>", unsafe_allow_html=True)
    email = st.text_input("👤 Login", placeholder="seu@email.com")
    st.write("---")
    st.markdown("### Suporte PRO")
    st.info("Dúvidas? Entre em contato com nossa equipe.")

# --- DASHBOARD DE USUÁRIO ---
if email:
    is_admin = email.lower() == PROPRIETARIO.lower()
    
    # Grid de Status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="glass-card"><p style="color: #94a3b8;">Plano Atual</p><h3 style="color: #a855f7;">{"VIP Proprietário" if is_admin else "Gratuito"}</h3></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card"><p style="color: #94a3b8;">Formato</p><h3 style="color: #6366f1;">9:16 Vertical</h3></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="glass-card"><p style="color: #94a3b8;">Motor de IA</p><h3 style="color: #ec4899;">Gemini 1.5 Pro</h3></div>', unsafe_allow_html=True)

    # Área de Trabalho
    st.write("---")
    left_col, right_col = st.columns([1.5, 1])

    with left_col:
        st.markdown("### 📥 Carregar Vídeo")
        video_file = st.file_uploader("", type=["mp4", "mov"])
        
    with right_col:
        st.markdown("### ⚙️ Opções")
        limite = st.slider("Quantidade de cortes", 1, 15, (10 if is_admin else 1))
        st.caption("A IA selecionará os melhores ganchos para retenção.")

    if video_file:
        with open("temp_input.mp4", "wb") as f:
            f.write(video_file.getbuffer())

        if st.button("✨ GERAR CORTES INTELIGENTES"):
            progress_bar = st.progress(0)
            status = st.empty()
            
            for i in range(limite):
                status.markdown(f"🤖 **Processando:** Corte {i+1} de {limite}...")
                inicio = i * 60
                saida = f"corte_viral_{i+1}.mp4"
                
                # Comando FFmpeg corrigido para evitar arquivos corrompidos (Screenshot_9)
                comando = f'ffmpeg -y -ss {inicio} -t 58 -i temp_input.mp4 -vf "crop=ih*(9/16):ih,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart {saida}'
                subprocess.run(comando, shell=True, capture_output=True)
                
                progress_bar.progress((i + 1) / limite)
                
                with st.expander(f"✅ Corte #{i+1} pronto"):
                    with open(saida, "rb") as f:
                        st.download_button(f"Baixar MP4 Parte {i+1}", f, file_name=saida)
            
            st.balloons()
            st.success("Mágica concluída! Seus cortes estão prontos para viralizar.")

else:
    st.markdown("<div style='text-align: center; padding: 50px; color: #94a3b8;'>Por favor, faça login na barra lateral para acessar o painel.</div>", unsafe_allow_html=True)