import streamlit as st
from database import criar_tabelas, conectar

st.set_page_config(
    page_title="Sistema Financeiro",
    page_icon="💰",
    layout="wide"
)

criar_tabelas()

# Estados
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"

if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""

# --------------------- LOGIN ESTILIZADO --------------------- #
def mostrar_login():
    st.title("Login Financeiro 💰")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        dados = cursor.fetchone()
        conn.close()

        if dados:
            st.session_state["logado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["pagina"] = "Dashboard"
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

    st.write("---")

    # 👉 Aqui está o botão que você pediu
    if st.button("Criar conta"):
        st.session_state["pagina"] = "registro"
        st.rerun()


# --------------------- REGISTRO --------------------- #
def mostrar_registro():
    st.title("Criar Conta 👤")

    user = st.text_input("Novo usuário")
    pwd = st.text_input("Senha", type="password")

    if st.button("Registrar"):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (user, pwd))
            conn.commit()
            st.success("Conta criada com sucesso! Faça login.")
            st.session_state["pagina"] = "login"
            st.rerun()
        except:
            st.error("Usuário já existe.")
        conn.close()

    if st.button("Voltar ao login"):
        st.session_state["pagina"] = "login"
        st.rerun()


# --------------------- ÁREA LOGADA --------------------- #
def mostrar_area_logada():

    st.sidebar.title(f"Bem-vindo, {st.session_state['usuario']} 👋")

    escolha = st.sidebar.radio(
        "Menu",
        ["Dashboard", "Despesas", "Entradas", "Configurações", "Logout"]
    )

    if escolha == "Dashboard":
        st.title("📊 Dashboard")
        st.write("Aqui você verá gráficos e dados financeiros.")

    elif escolha == "Despesas":
        st.title("💸 Despesas")
        st.write("Listagem de despesas aqui.")

    elif escolha == "Entradas":
        st.title("💰 Entradas")
        st.write("Listagem de entradas aqui.")

    elif escolha == "Configurações":
        st.title("⚙ Configurações")
        st.write("Configurações do sistema.")

    elif escolha == "Logout":
        st.session_state["logado"] = False
        st.session_state["pagina"] = "login"
        st.session_state["usuario"] = ""
        st.rerun()


def carregar_tela():
    if not st.session_state["logado"]:
        if st.session_state["pagina"] == "login":
            mostrar_login()
        else:
            mostrar_registro()
    else:
        mostrar_area_logada()


carregar_tela()
