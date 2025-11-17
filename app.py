import streamlit as st
import sqlite3
import base64

# -------------------------
# Função para carregar imagem como base64
# -------------------------
def load_image_base64(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

img_base64 = load_image_base64("hemacia.png")

# -------------------------
# CSS do fundo com opacidade suave
# -------------------------
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.25; /* opacidade suave */
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# -------------------------
# Banco de Dados
# -------------------------
def conectar():
    return sqlite3.connect("banco_hemocentro.db")

def criar_tabela():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                tipo_sanguineo TEXT NOT NULL
            );
        """)
        conn.commit()

criar_tabela()

# -------------------------
# Interface
# -------------------------
st.title("Cadastro de Doadores")

menu = ["Cadastrar", "Listar", "Remover"]
opcao = st.sidebar.selectbox("Menu", menu)

# -------------------------
# CADASTRAR
# -------------------------
if opcao == "Cadastrar":
    st.header("Cadastrar novo doador")

    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=0, max_value=120)
    tipo = st.text_input("Tipo Sanguíneo")

    if st.button("Salvar"):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO doadores (nome, idade, tipo_sanguineo) VALUES (?, ?, ?)",
                (nome, idade, tipo)
            )
            conn.commit()
        st.success("Doador cadastrado com sucesso!")

# -------------------------
# LISTAR
# -------------------------
elif opcao == "Listar":
    st.header("Lista de Doadores")

    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doadores")
        dados = cursor.fetchall()

    if dados:
        for d in dados:
            st.write(f"**ID:** {d[0]} | **Nome:** {d[1]} | **Idade:** {d[2]} | **Tipo:** {d[3]}")
    else:
        st.info("Nenhum doador cadastrado ainda.")

# -------------------------
# REMOVER
# -------------------------
elif opcao == "Remover":
    st.header("Remover Doador")

    id_remover = st.number_input("ID do doador a remover", min_value=1)

    if st.button("Remover"):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doadores WHERE id = ?", (id_remover,))
            conn.commit()

        st.success("Doador removido com sucesso!")
