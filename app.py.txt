import streamlit as st
import os
import subprocess
import time

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="CorteViral AI - Sua Fábrica de Shorts", layout="wide")

# --- SIMULAÇÃO DE BANCO DE DADOS ---
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {"admin": "123", "pro": "pro123"} # Exemplo
if 'logado' not in st.session_state:
    st.session_state['logado'] = False
if 'plano' not in st.session_state:
    st.session_state['plano'] = "Gratuito"

# --- TELA DE LOGIN E CADASTRO ---
def tela_login():
    st.title("🚀 CorteViral AI")
    aba1, aba2 = st.tabs(["Login", "Criar Conta"])
    
    with aba1:
        user = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if user in st.session_state['usuarios'] and st.session_state['usuarios'][user] == senha:
                st.session_state['logado'] = True
                st.session_state['plano'] = "Pro" if "pro" in user else "Gratuito"
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos")

    with aba2:
        st.write("Cadastre-se para começar a criar cortes virais.")
        novo_user = st.text_input("Novo Usuário")
        nova_senha = st.text_input("Nova Senha", type="password")
        plano_escolhido = st.radio("Escolha seu plano:", ["Gratuito (Limitado)", "Pro (R$ 49,90/mês)"])
        if st.button("Finalizar Cadastro"):
            st.success("Conta criada! Agora faça o login.")

# --- LÓGICA DE PROCESSAMENTO ---
def processar_video(video_path, num_cortes):
    pasta = "saida_cortes"
    if not os.path.exists(pasta): os.makedirs(pasta)
    
    for i in range(num_cortes):
        inicio = i * 60
        saida = f"{pasta}/corte_{i+1}.mp4"
        # Comando FFmpeg Profissional
        comando = f'ffmpeg -y -ss {inicio} -t 59 -i "{video_path}" -vf "crop=ih*(9/16):ih,scale=1080:1920" -c:v libx264 -preset ultrafast -pix_fmt yuv420p "{saida}"'
        subprocess.run(comando, shell=True)
        st.write(f"✅ Corte {i+1} finalizado...")
    
    return pasta

# --- DASHBOARD PRINCIPAL ---
if not st.session_state['logado']:
    tela_login()
else:
    st.sidebar.title(f"Bem-vindo!")
    st.sidebar.write(f"Plano Atual: **{st.session_state['plano']}**")
    if st.sidebar.button("Sair"):
        st.session_state['logado'] = False
        st.rerun()

    st.title("🎬 Gerador de Cortes Automáticos")
    
    upload = st.file_uploader("Suba seu vídeo longo (MP4, MOV)", type=["mp4", "mov"])
    
    if upload:
        with open("temp_video.mp4", "wb") as f:
            f.write(upload.getbuffer())
        
        limite = 1 if st.session_state['plano'] == "Gratuito" else 10
        st.info(f"Seu plano permite gerar até {limite} cortes por vez.")
        
        if st.button(f"Gerar {limite} Cortes"):
            with st.spinner("A IA está trabalhando nos seus cortes..."):
                pasta_resultado = processar_video("temp_video.mp4", limite)
                
                # Compactar para Download
                subprocess.run(f"zip -r resultados.zip {pasta_resultado}", shell=True)
                
                with open("resultados.zip", "rb") as f:
                    st.download_button("📥 Baixar Todos os Cortes (ZIP)", f, file_name="meus_cortes.zip")
                st.success("Processamento concluído!")

    if st.session_state['plano'] == "Gratuito":
        st.warning("🚀 Quer gerar 10 cortes de uma vez e sem marca d'água? Assine o plano PRO.")