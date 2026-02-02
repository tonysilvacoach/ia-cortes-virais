import streamlit as st
import subprocess
import os

# --- CONFIGURAÇÕES DE ESTILO (CSS) ---
st.set_page_config(page_title="CorteViral PRO - IA Video Editor", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        border: none;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    .upload-box {
        border: 2px dashed #4F8BF9;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NEGÓCIO ---
PROPRIETARIO = "niltonrosa71@gmail.com"

# Sidebar com Branding
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3669/3669914.png", width=100) # Ícone Pro
    st.title("CorteViral PRO")
    st.write("---")
    email = st.text_input("👤 Login de Usuário", placeholder="seu@email.com")

# Corpo Principal
if email:
    if email.lower() == PROPRIETARIO.lower():
        st.markdown(f"### 👑 Painel do Proprietário")
        st.success("Acesso Ilimitado Liberado para Nilton Rosa.")
        limite = 15 
        plano = "PRO"
    else:
        st.markdown(f"### 🚀 Dashboard de Edição")
        st.info("Plano: Gratuito (1 corte de teste)")
        limite = 1
        plano = "FREE"

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 📤 1. Carregar Conteúdo")
        upload = st.file_uploader("", type=["mp4", "mov"])
        
    with col2:
        st.markdown("#### 🛠️ 2. Configurações")
        st.write(f"Cortes a serem gerados: **{limite}**")
        st.write(f"Formato: **9:16 (TikTok/Reels/Shorts)**")

    if upload:
        with open("video_input.mp4", "wb") as f:
            f.write(upload.getbuffer())
        
        if st.button("✨ GERAR CORTES VIRAIS AGORA"):
            # Barra de progresso profissional
            progresso = st.progress(0)
            for i in range(limite):
                inicio = i * 60
                saida = f"corte_{i+1}.mp4"
                
                # Motor FFmpeg Blindado
                comando = f'ffmpeg -y -ss {inicio} -t 59 -i video_input.mp4 -vf "crop=ih*(9/16):ih,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart {saida}'
                subprocess.run(comando, shell=True)
                
                progresso.progress((i + 1) / limite)
                st.write(f"✅ Corte {i+1} finalizado!")
                
                with open(saida, "rb") as f:
                    st.download_button(f"📥 Baixar Corte {i+1}", f, file_name=saida)
            
            st.balloons()
            st.success("Todos os vídeos foram processados com sucesso!")
else:
    st.warning("⚠️ Por favor, faça login com seu e-mail para desbloquear a ferramenta.")
