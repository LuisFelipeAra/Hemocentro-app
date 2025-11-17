import streamlit as st
import sqlite3
from datetime import datetime

# Conexão com o BD
def conectar():
    return sqlite3.connect("banco_hemocentro.db")

# Criar tabelas
def criar_tabelas():
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER,
                tipo_sanguineo TEXT,
                cidade TEXT,
                telefone TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hemocentros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                endereco TEXT,
                cidade TEXT,
                telefone TEXT
            )
        ''')

        cursor.execute('''
            CREATE TA
