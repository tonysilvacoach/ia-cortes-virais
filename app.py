import streamlit as st
import subprocess
import os
import time

# --- CONFIGURAÇÃO DA PÁGINA (ESTILO REKA) ---
st.set_page_config(page_title="ViralCut AI | Smart Clipping", layout="wide", initial_sidebar_state="expanded")

# --- CSS PERSONALIZADO (DARK MODE & GLASSMORPHISM) ---
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #e5e7eb; }
    [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #222; }
    
    /* Card de Download Estilo Reka */
    .download-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Botões de Gradiente */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white; border: none; border-radius: 8px;
        padding: 10px 20px; font-weight: 600; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE ACESSO VIP ---
PROPRIETARIO = "niltonrosa71@gmail.com" #

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #a855f7;'>ViralCut AI</h2>", unsafe_allow_html=True)
    user_email = st.text_input("🔑 E-mail de Acesso", placeholder="seu@email.com")
    st.write("---")
    st.markdown("### 💎 Plano")
    if user_email.lower() == PROPRIETARIO.lower():
        st.success("Proprietário VIP")
        limite_cortes = 20
    else:
        st.info("Plano Gratuito")
        limite_cortes = 1

# --- DASHBOARD PRINCIPAL ---
if user_email:
    st.markdown(f"## Bem-vindo, {user_email.split('@')[0]}!")
    
    # Layout em Colunas
    col_upload, col_settings = st.columns([1.5, 1])
    
    with col_upload:
        st.markdown("### 🎥 Carregar Vídeo")
        video_file = st.file_uploader("", type=["mp4", "mov"])
        
    with col_settings:
        st.markdown("### ⚙️ Configurações")
        qtd = st.number_input("Número de cortes", min_value=1, max_value=limite_cortes, value=1)
        st.caption(f"Limite do seu plano: {limite_cortes} cortes por vídeo.")

    if video_file:
        input_path = "video_base.mp4"
        with open(input_path, "wb") as f:
            f.write(video_file.getbuffer())

        if st.button("✨ GERAR CORTES INTELIGENTES"):
            st.write("---")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # CRIAMOS UMA LISTA PARA ARMAZENAR OS DADOS DOS CORTES
            cortes_gerados = []

            for i in range(qtd):
                inicio = i * 60
                saida = f"corte_viral_{i+1}.mp4"
                
                status_text.markdown(f"🤖 **IA Processando:** Gerando corte {i+1} de {qtd}...")
                
                # Comando FFmpeg corrigido para garantir compatibilidade
                comando = f'ffmpeg -y -ss {inicio} -t 58 -i {input_path} -vf "crop=ih*(9/16):ih,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart {saida}'
                
                result = subprocess.run(comando, shell=True, capture_output=True)
                
                if os.path.exists(saida):
                    cortes_gerados.append(saida)
                
                progress_bar.progress((i + 1) / qtd)
            
            # --- ÁREA DE DOWNLOAD (EXTERNAMENTE AO LOOP PARA NÃO SUMIR) ---
            st.markdown("### 📥 Seus Cortes Prontos")
            if not cortes_gerados:
                st.error("Erro ao gerar arquivos. Verifique o formato do vídeo.")
            else:
                for idx, arquivo in enumerate(cortes_gerados):
                    with open(arquivo, "rb") as f:
                        st.download_button(
                            label=f"⬇️ Baixar Corte #{idx+1}",
                            data=f,
                            file_name=arquivo,
                            mime="video/mp4",
                            key=f"dl_{idx}"
                        )
                st.balloons()
else:
    st.warning("⚠️ Insira seu e-mail na barra lateral para acessar o painel.")
