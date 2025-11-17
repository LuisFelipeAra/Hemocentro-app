import streamlit as st
import sqlite3
from datetime import datetime

# ===========================
#  CSS + IMAGEM DE FUNDO
# ===========================
st.set_page_config(page_title="Sistema de Hemocentros", page_icon="🩸", layout="wide")

st.markdown("""
    <style>
        body {
            background-image: url('https://images.unsplash.com/photo-1582719478250-c89cae4dc85b');
            background-size: cover;
        }
        .stApp {
            background: rgba(255, 255, 255, 0.80);
            backdrop-filter: blur(4px);
        }
    </style>
""", unsafe_allow_html=True)

# ===========================
#  BANCO DE DADOS
# ===========================
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
                FOREIGN KEY(id_hemocentro) REFERENCES hemocentros(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_hemocentro INTEGER,
                tipo_sanguineo TEXT NOT NULL,
                quantidade INTEGER DEFAULT 0,
                FOREIGN KEY(id_hemocentro) REFERENCES hemocentros(id)
            )
        """)

        conn.commit()

criar_tabelas()

# ===========================
#  LAYOUT
# ===========================
st.title("🩸 Sistema de Hemocentros")

menu = st.sidebar.selectbox("Navegação", [
    "🏠 Início",
    "🧍 Doadores",
    "🏥 Hemocentros",
    "💉 Doações",
    "📦 Estoque"
])

# ===========================
#  INÍCIO
# ===========================
if menu == "🏠 Início":
    st.markdown("### Bem-vindo ao Sistema de Gerenciamento de Hemocentros!")

# ===========================
#  DOADORES
# ===========================
elif menu == "🧍 Doadores":
    st.subheader("Cadastro de Doadores")

    nome = st.text_input("Nome do Doador")
    idade = st.number_input("Idade", min_value=18, max_value=100)
    tipo = st.selectbox("Tipo Sanguíneo", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    cidade = st.text_input("Cidade")
    telefone = st.text_input("Telefone")

    if st.button("Salvar Doador"):
        if nome.strip():
            with conectar() as conn:
                conn.execute(
                    "INSERT INTO doadores (nome, idade, tipo_sanguineo, cidade, telefone) VALUES (?, ?, ?, ?, ?)",
                    (nome, idade, tipo, cidade, telefone)
                )
                conn.commit()
            st.success(f"Doador {nome} cadastrado com sucesso! ✅")
        else:
            st.warning("Digite um nome válido.")

    st.markdown("---")
    st.subheader("Lista de Doadores")

    with conectar() as conn:
        doadores = conn.execute("SELECT * FROM doadores").fetchall()

    if doadores:
        st.dataframe(doadores, use_container_width=True)

        st.markdown("### Remover Doador")
        selecionado = st.selectbox("Escolha", [f"{d[0]} - {d[1]}" for d in doadores])

        if st.button("Remover"):
            try:
                id_d = int(selecionado.split(" - ")[0])
                with conectar() as conn:
                    conn.execute("DELETE FROM doadores WHERE id = ?", (id_d,))
                    conn.commit()
                st.success("Doador removido!")
            except:
                st.error("Erro ao remover.")
    else:
        st.info("Nenhum doador cadastrado.")

# ===========================
#  HEMOCENTROS
# ===========================
elif menu == "🏥 Hemocentros":
    st.subheader("Cadastro de Hemocentros")

    nome_h = st.text_input("Nome")
    endereco_h = st.text_input("Endereço")
    cidade_h = st.text_input("Cidade")
    telefone_h = st.text_input("Telefone")

    if st.button("Salvar Hemocentro"):
        with conectar() as conn:
            conn.execute(
                "INSERT INTO hemocentros (nome, endereco, cidade, telefone) VALUES (?, ?, ?, ?)",
                (nome_h, endereco_h, cidade_h, telefone_h)
            )
            conn.commit()
