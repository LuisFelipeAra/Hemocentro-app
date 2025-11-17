import streamlit as st
import sqlite3
from datetime import datetime

# ======================================
#   IMAGEM DE FUNDO (APENAS ALTERAÇÃO)
# ======================================
st.set_page_config(page_title="Sistema de Hemocentros", page_icon="🩸", layout="wide")

st.markdown("""
    <style>
        body {
            background-image: url('https://anadem.com.br/wp-content/uploads/2016/11/hemacia.png');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }
        .stApp {
            background: rgba(255, 255, 255, 0.80);
            backdrop-filter: blur(4px);
        }
    </style>
""", unsafe_allow_html=True)

# ======================================
#   BANCO DE DADOS
# ======================================
def conectar():
    return sqlite3.connect("banco_hemocentro.db")

def criar_tabelas():
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER,
                tipo_sanguineo TEXT,
                cidade TEXT,
                telefone TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hemocentros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                endereco TEXT,
                cidade TEXT,
                telefone TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_doador INTEGER,
                id_hemocentro INTEGER,
                data_doacao TEXT,
                FOREIGN KEY(id_doador) REFERENCES doadores(id),
                FOREIGN KEY(id_hemocentro) REFERENCES h_
