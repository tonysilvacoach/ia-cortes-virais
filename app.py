import streamlit as st
import subprocess
import os

# Configuração de Segurança (Secrets)
if "GEMINI_API_KEY" in st.secrets:
    import google.generativeai as genai
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🎬 CorteViral AI - Versão PRO")

# Interface de Login Simples para Venda
user_tipo = st.sidebar.radio("Tipo de Acesso", ["Gratuito", "PRO"])

upload = st.file_uploader("Suba seu vídeo", type=["mp4", "mov"])

if upload:
    with open("video_original.mp4", "wb") as f:
        f.write(upload.getbuffer())
    
    num_cortes = 1 if user_tipo == "Gratuito" else 10
    st.info(f"Gerando {num_cortes} cortes para o plano {user_tipo}...")

    if st.button("Iniciar Processamento"):
        for i in range(num_cortes):
            inicio = i * 60
            saida = f"corte_{i+1}.mp4"
            # Comando FFmpeg com correção de codec para evitar erro 0xc10100be
            comando = f'ffmpeg -y -ss {inicio} -t 59 -i video_original.mp4 -vf "crop=ih*(9/16):ih,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart {saida}'
            subprocess.run(comando, shell=True)
            st.success(f"Corte {i+1} pronto!")
            with open(saida, "rb") as f:
                st.download_button(f"Baixar Corte {i+1}", f, file_name=saida)
