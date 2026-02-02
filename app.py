import streamlit as st
import subprocess
import os

# --- 1. CONFIGURAÇÃO DE INTERFACE ---
st.set_page_config(page_title="ViralCut AI PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; font-family: 'Inter', sans-serif; }
    .dashboard-card { background: #111; border: 1px solid #222; padding: 20px; border-radius: 12px; text-align: center; }
    .stButton>button { background: linear-gradient(90deg, #6366f1, #a855f7); color: white; border: none; border-radius: 8px; width: 100%; height: 3.5rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 2. LOGICA DE ACESSO ---
PROPRIETARIO = "niltonrosa71@gmail.com"

with st.sidebar:
    st.markdown("<h2 style='color: #a855f7;'>ViralCut AI</h2>", unsafe_allow_html=True)
    email = st.text_input("👤 Login", placeholder="seu@email.com")
    is_admin = (email.lower() == PROPRIETARIO.lower()) if email else False

# --- 3. DASHBOARD ---
if email:
    st.markdown(f"## Dashboard: {'Proprietário VIP' if is_admin else 'Usuário'}")
    
    # CORREÇÃO DO NAMEERROR: Definindo as 3 colunas corretamente
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="dashboard-card"><p>Plano</p><h3>{"PRO" if is_admin else "FREE"}</h3></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="dashboard-card"><p>Formato</p><h3>9:16 Vertical</h3></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="dashboard-card"><p>Motor</p><h3 style="color:#22c55e;">Ativo</h3></div>', unsafe_allow_html=True)

    st.write("---")
    
    # 4. PROCESSAMENTO
    video_file = st.file_uploader("Suba seu vídeo para processar", type=["mp4", "mov"])

    if video_file:
        input_path = os.path.join(os.getcwd(), "video_input.mp4")
        with open(input_path, "wb") as f:
            f.write(video_file.getbuffer())
        
        if st.button("✨ GERAR CORTE INTELIGENTE"):
            saida = os.path.join(os.getcwd(), "resultado_viral.mp4")
            
            # Comando formatado como LISTA para evitar erros de aspas (SyntaxError)
            comando = [
                'ffmpeg', '-y', '-i', input_path, 
                '-t', '15', 
                '-vf', 'crop=ih*(9/16):ih,scale=1080:1920', 
                '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', 
                '-c:a', 'aac', '-movflags', '+faststart', saida
            ]
            
            with st.spinner("IA Renderizando..."):
                result = subprocess.run(comando, capture_output=True, text=True)
            
            if os.path.exists(saida):
                st.success("Vídeo processado com sucesso!")
                with open(saida, "rb") as f:
                    st.download_button("📥 Baixar Vídeo Viral", f, file_name="viral_cut.mp4")
            else:
                st.error("Erro no motor de vídeo. Verifique o log.")
                st.code(result.stderr)
else:
    st.info("Por favor, insira seu e-mail para desbloquear as ferramentas.")
