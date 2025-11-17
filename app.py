import streamlit as st
import sqlite3
from datetime import datetime

#IMAGEM DE FUNDO
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
            background: transparent !important;
        }
    </style>
""", unsafe_allow_html=True)



#BD
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
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hemocentros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                endereco TEXT,
                cidade TEXT,
                telefone TEXT
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_doador INTEGER,
                id_hemocentro INTEGER,
                data_doacao TEXT,
                FOREIGN KEY(id_doador) REFERENCES doadores(id),
                FOREIGN KEY(id_hemocentro) REFERENCES hemocentros(id)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_hemocentro INTEGER,
                tipo_sanguineo TEXT NOT NULL,
                quantidade INTEGER DEFAULT 0,
                FOREIGN KEY(id_hemocentro) REFERENCES hemocentros(id)
            );
        """)

        conn.commit()

criar_tabelas()

#LAYOUT
st.title("🩸 Sistema de Hemocentros")

menu = st.sidebar.selectbox(
    "Navegação",
    ["🏠 Início", "🧍 Doadores", "🏥 Hemocentros", "💉 Doações", "📦 Estoque"]
)

#INÍCIO
if menu == "🏠 Início":
    st.markdown("### Bem-vindo ao Sistema de Gerenciamento de Hemocentros!")

#DOADORES
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

        selecionado = st.selectbox("Selecione o doador para remover:", [f"{d[0]} - {d[1]}" for d in doadores])

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

#HEMOCENTROS
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
        st.success("Hemocentro salvo!")

    st.markdown("---")

    with conectar() as conn:
        hemocentros = conn.execute("SELECT * FROM hemocentros").fetchall()

    if hemocentros:
        st.dataframe(hemocentros, use_container_width=True)
    else:
        st.info("Nenhum hemocentro cadastrado.")


#DOAÇÕES
elif menu == "💉 Doações":
    st.subheader("Registro de Doações")

    with conectar() as conn:
        doadores = conn.execute("SELECT id, nome FROM doadores").fetchall()
        hemocentros = conn.execute("SELECT id, nome FROM hemocentros").fetchall()

    if not doadores or not hemocentros:
        st.warning("Cadastre ao menos um doador e um hemocentro.")
    else:
        d = st.selectbox("Doador", [f"{i[0]} - {i[1]}" for i in doadores])
        h = st.selectbox("Hemocentro", [f"{i[0]} - {i[1]}" for i in hemocentros])

        if st.button("Registrar Doação"):
            id_d = int(d.split(" - ")[0])
            id_h = int(h.split(" - ")[0])
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with conectar() as conn:
                conn.execute(
                    "INSERT INTO doacoes (id_doador, id_hemocentro, data_doacao) VALUES (?, ?, ?)",
                    (id_d, id_h, data)
                )
                conn.commit()

            st.success("Doação registrada!")

#ESTOQUE
elif menu == "📦 Estoque":
    st.subheader("Estoque de Sangue")

    with conectar() as conn:
        hemocentros = conn.execute("SELECT id, nome FROM hemocentros").fetchall()

    if not hemocentros:
        st.warning("Cadastre um hemocentro primeiro.")
    else:
        h = st.selectbox("Hemocentro", [f"{i[0]} - {i[1]}" for i in hemocentros])
        id_h = int(h.split(" - ")[0])

        tipo = st.selectbox("Tipo Sanguíneo", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        qtd = st.number_input("Quantidade", min_value=1)

        if st.button("Adicionar"):
            with conectar() as conn:
                ex = conn.execute(
                    "SELECT quantidade FROM estoque WHERE id_hemocentro = ? AND tipo_sanguineo = ?",
                    (id_h, tipo)
                ).fetchone()

                if ex:
                    conn.execute(
                        "UPDATE estoque SET quantidade = ? WHERE id_hemocentro = ? AND tipo_sanguineo = ?",
                        (ex[0] + qtd, id_h, tipo)
                    )
                else:
                    conn.execute(
                        "INSERT INTO estoque (id_hemocentro, tipo_sanguineo, quantidade) VALUES (?, ?, ?)",
                        (id_h, tipo, qtd)
                    )
                conn.commit()

            st.success("Estoque atualizado!")

        st.markdown("---")
        st.subheader("📊 Estoque Atual")

        with conectar() as conn:
            tabela = conn.execute("""
                SELECT hemocentros.nome, estoque.tipo_sanguineo, estoque.quantidade
                FROM estoque
                JOIN hemocentros ON hemocentros.id = estoque.id_hemocentro
                WHERE hemocentros.id = ?
            """, (id_h,)).fetchall()

        if tabela:
            st.dataframe(tabela, use_container_width=True)
        else:
            st.info("Nenhum estoque registrado.")


