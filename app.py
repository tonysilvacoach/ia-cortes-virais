import streamlit as st
import google.generativeai as genai
import subprocess
import os
import time

# --- DESIGN HEYGEN / VEO 3 STYLE ---
st.set_page_config(page_title="VeoLab AI PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    .canvas-container { border: 1px solid #e2e8f0; border-radius: 12px; padding: 30px; background: white; text-align: center; }
    .stButton>button { background-color: #000000; color: white; border-radius: 20px; font-weight: 600; width: 100%; height: 3.5rem; }
    .stProgress > div > div > div > div { background-color: #a855f7; } /* Cor da barra de progresso */
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API GEMINI ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
else:
    st.error("Erro: 'GEMINI_API_KEY' não encontrada nos Secrets.")
    model = None

# --- SIDEBAR (ASSETS) ---
with st.sidebar:
    st.title("🧪 VeoLab")
    email = st.text_input("Identidade", value="niltonrosa71@gmail.com")
    st.write("---")
    menu = st.radio("Menu", ["🏠 Home", "🎬 Criar Vídeo", "👤 Avatares"])

# --- ÁREA CENTRAL ---
if menu == "🎬 Criar Vídeo":
    st.markdown("<h2 style='text-align: center;'>Transforme ideias em produção real com IA</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
        tab_txt, tab_img = st.tabs(["✍️ Texto", "🖼️ Imagem"])
        
        prompt_text = ""
        uploaded_image = None

        with tab_txt:
            prompt_text = st.text_area("Descreva seu vídeo...", placeholder="Ex: Um pôr do sol vibrante na praia, com ondas calmas e coqueiros balançando ao vento.")
        with tab_img:
            uploaded_image = st.file_uploader("Upload de imagem base (opcional)", type=["jpg", "png"])
            if uploaded_image:
                st.image(uploaded_image, caption="Imagem de fundo", use_column_width=True)
                prompt_text = st.text_area("O que deve acontecer nesta imagem?", value=prompt_text, placeholder="Ex: Animar as ondas e o movimento do coqueiro na imagem acima.")

        if st.button("✨ GERAR VÍDEO AGORA"):
            if not model:
                st.error("A API Gemini não está configurada. Verifique os Secrets.")
            elif not prompt_text and not uploaded_image:
                st.warning("Por favor, forneça uma descrição ou uma imagem.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("1/3 - IA analisando seu prompt...")
                progress_bar.progress(33)
                
                # --- PASSO 1: GERAR ROTEIRO VISUAL COM GEMINI ---
                try:
                    full_prompt = f"Crie um roteiro visual detalhado para um vídeo curto (5 segundos) sobre: '{prompt_text}'. Descreva 3 quadros principais, com detalhes visuais e o que se move em cada um. Cada quadro deve ser descritivo o suficiente para gerar uma imagem."
                    
                    response = model.generate_content(full_prompt)
                    visual_script = response.text
                    st.success("Roteiro visual gerado pela IA:")
                    st.info(visual_script)
                except Exception as e:
                    st.error(f"Erro ao gerar roteiro visual com Gemini: {e}")
                    status_text.text("Falha ao gerar roteiro.")
                    progress_bar.progress(0)
                    st.stop()
                
                status_text.text("2/3 - IA criando os frames (simulado)...")
                progress_bar.progress(66)
                
                # --- PASSO 2: SIMULAR GERAÇÃO DE IMAGENS (PARA O FUTURO) ---
                # Neste ponto, em uma versão real, integraríamos uma API de Text-to-Image (DALL-E 3, Midjourney)
                # Por enquanto, vamos criar imagens de placeholder ou usar a imagem carregada
                
                # Criar um diretório temporário para as imagens
                temp_dir = "temp_frames"
                os.makedirs(temp_dir, exist_ok=True)
                
                frame_files = []
                for i in range(3): # 3 frames simulados
                    frame_path = os.path.join(temp_dir, f"frame_{i:02d}.png")
                    
                    if uploaded_image:
                        # Se houver imagem, usá-la como base para todos os frames (simulação)
                        from PIL import Image
                        img_base = Image.open(uploaded_image).resize((1280, 720))
                        img_base.save(frame_path)
                    else:
                        # Gerar imagem simples (tela preta com texto)
                        cmd_img = [
                            "ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=black:s=1280x720",
                            "-vf", f"drawtext=text='Frame {i+1} - {prompt_text[:20]}':fontcolor=white:x=(w-tw)/2:y=(h-th)/2:fontsize=30",
                            "-frames:v", "1", frame_path
                        ]
                        subprocess.run(cmd_img, check=True, capture_output=True)
                    frame_files.append(frame_path)
                    time.sleep(0.5) # Simula o tempo de geração de imagem

                status_text.text("3/3 - Montando o vídeo com FFmpeg...")
                progress_bar.progress(100)
                
                # --- PASSO 3: MONTAR O VÍDEO COM FFmpeg ---
                out_video = "veolab_prod.mp4"
                
                # Comando FFmpeg para montar vídeo a partir de imagens
                if frame_files:
                    cmd_video = [
                        "ffmpeg", "-y", "-framerate", "1", "-i", os.path.join(temp_dir, "frame_%02d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", out_video
                    ]
                    try:
                        result = subprocess.run(cmd_video, check=True, capture_output=True)
                        if result.returncode == 0 and os.path.exists(out_video):
                            st.video(out_video)
                            st.success("Vídeo gerado com sucesso!")
                            with open(out_video, "rb") as f:
                                st.download_button("📥 Baixar Produção", f, file_name=out_video)
                        else:
                            st.error(f"Erro na montagem do vídeo: {result.stderr}")
                    except Exception as e:
                        st.error(f"Falha no motor de vídeo: {e}")
                else:
                    st.error("Nenhuma imagem gerada para montar o vídeo.")
                
                # Limpar arquivos temporários
                for f in frame_files:
                    if os.path.exists(f):
                        os.remove(f)
                if os.path.exists(temp_dir):
                    os.rmdir(temp_dir)
        
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "👤 Avatares":
    st.subheader("Biblioteca de Avatares")
    st.info("Em breve: Clonagem de voz e imagem para os canais Notícias New e Habitus Milionário.")

st.markdown("---")
st.caption("VeoLab AI - Powered by Google Gemini. ✨")
