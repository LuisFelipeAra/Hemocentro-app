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
            CREATE TABLE IF NOT EXISTS doacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_doador INTEGER,
                id_hemocentro INTEGER,
                data_doacao TEXT,
                FOREIGN KEY(id_doador) REFERENCES doadores(id),
                FOREIGN KEY(id_hemocentro) REFERENCES hemocentros(id)
            )
        ''')
        conn.commit()

criar_tabelas()

# Layout principal
st.set_page_config(page_title="Sistema de Hemocentros", page_icon="🩸")
st.title("🩸 Sistema de Hemocentros")

menu = st.sidebar.selectbox("Navegação", ["🏠 Início", "🧍 Doadores", "🏥 Hemocentros", "💉 Doações"])

# Início
if menu == "🏠 Início":
    st.write("""
    ## Aqui você pode cadastrar doadores, hemocentros e registrar doações de sangue.
    """)

# Doadores
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
        doador_ids = [f"{d[0]} - {d[1]}" for d in doadores]
        doador_remover = st.selectbox("Selecione o doador a remover", doador_ids)

        if st.button("Remover Doador") and doador_remover:
            try:
                id_doador = int(doador_remover.split(" - ")[0])
                with conectar() as conn:
                    conn.execute("DELETE FROM doadores WHERE id = ?", (id_doador,))
                    conn.commit()
                st.success("Doador removido com sucesso! 🗑️")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao remover doador: {e}")
    else:
        st.info("Nenhum doador cadastrado ainda.")

# Hemocentros
elif menu == "🏥 Hemocentros":
    st.subheader("Cadastro de Hemocentros")

    nome_h = st.text_input("Nome do Hemocentro")
    endereco_h = st.text_input("Endereço")
    cidade_h = st.text_input("Cidade")
    telefone_h = st.text_input("Telefone")

    if st.button("Salvar Hemocentro"):
        if nome_h.strip():
            with conectar() as conn:
                conn.execute(
                    "INSERT INTO hemocentros (nome, endereco, cidade, telefone) VALUES (?, ?, ?, ?)",
                    (nome_h, endereco_h, cidade_h, telefone_h)
                )
                conn.commit()
            st.success(f"Hemocentro {nome_h} cadastrado com sucesso! ✅")
        else:
            st.warning("Digite um nome válido.")

    st.markdown("---")
    st.subheader("Lista de Hemocentros")

    with conectar() as conn:
        hemocentros = conn.execute("SELECT * FROM hemocentros").fetchall()

    if hemocentros:
        st.dataframe(hemocentros, use_container_width=True)

        st.markdown("### Remover Hemocentro")
        hemo_ids = [f"{h[0]} - {h[1]}" for h in hemocentros]
        hemo_remover = st.selectbox("Selecione o hemocentro a remover", hemo_ids)

        if st.button("Remover Hemocentro") and hemo_remover:
            try:
                id_hemocentro = int(hemo_remover.split(" - ")[0])
                with conectar() as conn:
                    conn.execute("DELETE FROM hemocentros WHERE id = ?", (id_hemocentro,))
                    conn.commit()
                st.success("Hemocentro removido com sucesso! 🗑️")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao remover hemocentro: {e}")
    else:
        st.info("Nenhum hemocentro cadastrado ainda.")

# Doações
elif menu == "💉 Doações":
    st.subheader("Registro de Doações")

    with conectar() as conn:
        doadores = conn.execute("SELECT id, nome FROM doadores").fetchall()
        hemocentros = conn.execute("SELECT id, nome FROM hemocentros").fetchall()

    if not doadores or not hemocentros:
        st.warning("Você precisa cadastrar ao menos um doador e um hemocentro antes de registrar uma doação.")
    else:
        doador_escolhido = st.selectbox("Selecione o Doador", [f"{d[0]} - {d[1]}" for d in doadores])
        hemocentro_escolhido = st.selectbox("Selecione o Hemocentro", [f"{h[0]} - {h[1]}" for h in hemocentros])

        if st.button("Registrar Doação"):
            id_doador = int(doador_escolhido.split(" - ")[0])
            id_hemocentro = int(hemocentro_escolhido.split(" - ")[0])
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with conectar() as conn:
                conn.execute(
                    "INSERT INTO doacoes (id_doador, id_hemocentro, data_doacao) VALUES (?, ?, ?)",
                    (id_doador, id_hemocentro, data)
                )
                conn.commit()
            st.success("Doação registrada com sucesso! 💉")

    st.markdown("---")
    st.subheader("Histórico de Doações")
    with conectar() as conn:
        registros = conn.execute('''
            SELECT d.id, doadores.nome, hemocentros.nome, d.data_doacao
            FROM doacoes d
            JOIN doadores ON d.id_doador = doadores.id
            JOIN hemocentros ON d.id_hemocentro = hemocentros.id
        ''').fetchall()

        if registros:
            st.dataframe(registros, use_container_width=True)
        else:
            st.info("Nenhuma doação registrada ainda.")
