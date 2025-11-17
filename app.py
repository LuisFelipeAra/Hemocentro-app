import streamlit as st
import sqlite3
from datetime import datetime
import base64

# ========= FUNÇÃO PARA CARREGAR A IMAGEM EM BASE64 =========
def load_image_base64(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# Carrega a imagem que está no MESMO diretório do app.py
img_base64 = load_image_base64("hemacia.png")

# ========= CONFIGURAÇÃO DA PÁGINA =========
st.set_page_config(page_title="Sistema de Hemocentros", page_icon="🩸", layout="wide")

# ========= CSS DO FUNDO =========
st.markdown(
    f"""
    <style>
        body {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        .stApp {{
