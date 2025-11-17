import streamlit as st
import base64
import os

def load_image_base64(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# DEBUG TEMPORÁRIO → ver se a imagem existe no diretório
st.write("Arquivos no diretório:", os.listdir())

# Carregar a imagem
img_base64 = load_image_base64("hemacia.png")

# Aplicar imagem como fundo
page_bg_img = f"""
<style>
.stApp {{
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Seu conteúdo Streamlit
st.title("Sistema de Hemocentro")
