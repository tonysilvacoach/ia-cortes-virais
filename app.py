import streamlit as st
import subprocess
import os

# --- CONFIGURAÇÃO DE ACESSO ---
PROPRIETARIO = "niltonrosa71@gmail.com"
LIMITE_GRATUITO = 2  # Créditos totais para novos usuários por sessão

if 'creditos_usados' not in st.session_state:
    st.session_state['creditos_usados'] = 0

# --- LÓGICA DO DASHBOARD ---
with st.sidebar:
    st.markdown("<h2 style='color: #a855f7;'>Sua Conta</h2>", unsafe_allow_html=True)
    email = st.text_input("👤 E-mail cadastrado", placeholder="ex@email.com")

if email:
    is_admin = email.lower() == PROPRIETARIO.lower()
    
    # Cálculo de Créditos Restantes
    if is_admin:
        creditos_restantes = "∞ (Ilimitado)"
        pode_processar = True
    else:
        restantes = LIMITE_GRATUITO - st.session_state['creditos_usados']
        creditos_restantes = str(max(0, restantes))
        pode_processar = restantes > 0

    # Cards Visuais (Estilo ViralCut)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="glass-card"><p>Plano</p><h3>{"PRO / ADM" if is_admin else "Gratuito"}</h3></div>', unsafe_allow_html=True)
    with col2:
        cor_credito = "#22c55e" if pode_processar else "#ef4444"
        st.markdown(f'<div class="glass-card"><p>Créditos</p><h3 style="color: {cor_credito};">{creditos_restantes}</h3></div>', unsafe_allow_html=True)

    if not pode_processar:
        st.error("⚠️ Seus créditos gratuitos acabaram! Assine o Plano PRO para continuar.")
        st.button("💎 Fazer Upgrade Agora (R$ 49,90)")
    else:
        # Área de Upload e Processamento
        video_file = st.file_uploader("Suba seu vídeo", type=["mp4", "mov"])
        
        if video_file and st.button("✨ GERAR CORTE"):
            # Lógica de processamento...
            # (Adicione o comando FFmpeg aqui como nos passos anteriores)
            
            # Consumo de crédito
            if not is_admin:
                st.session_state['creditos_usados'] += 1
            st.success("Corte concluído com sucesso!")
