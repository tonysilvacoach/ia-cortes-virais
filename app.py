import streamlit as st
import subprocess
import os

# --- 1. CONFIGURAÇÕES DO PROPRIETÁRIO ---
# Este é o seu acesso VIP para os canais Notícias New e Habitus Milionário
PROPRIETARIO_EMAIL = "niltonrosa71@gmail.com" 

st.set_page_config(page_title="CorteViral AI - Dashboard", layout="centered")

# --- 2. ÁREA DE ACESSO ---
st.title("🎬 CorteViral AI")
email_usuario = st.text_input("Digite seu e-mail para acessar o sistema:")

if email_usuario:
    # Verificação de Proprietário
    if email_usuario.lower() == PROPRIETARIO_EMAIL.lower():
        st.success("👑 Bem-vindo, Proprietário! Acesso ILIMITADO liberado.")
        limite_cortes = 20  # Você pode gerar muitos cortes de uma vez
        plano = "PRO"
    else:
        st.info("Acesso Gratuito: 1 corte por vídeo (Limite de teste)")
        limite_cortes = 1
        plano = "FREE"

    # --- 3. UPLOAD E PROCESSAMENTO ---
    upload = st.file_uploader("Escolha seu vídeo longo", type=["mp4", "mov"])

    if upload:
        with open("video_temp.mp4", "wb") as f:
            f.write(upload.getbuffer())
        
        if st.button(f"Gerar {limite_cortes} Corte(s)"):
            for i in range(limite_cortes):
                inicio = i * 60
                saida = f"corte_{i+1}.mp4"
                
                # Comando FFmpeg blindado contra vídeos corrompidos
                comando = f'ffmpeg -y -ss {inicio} -t 59 -i video_temp.mp4 -vf "crop=ih*(9/16):ih,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart {saida}'
                
                with st.spinner(f"Processando corte {i+1}..."):
                    subprocess.run(comando, shell=True)
                
                with open(saida, "rb") as f:
                    st.download_button(f"📥 Baixar Corte {i+1}", f, file_name=saida)
            
            st.success("Cortes finalizados com sucesso!")
