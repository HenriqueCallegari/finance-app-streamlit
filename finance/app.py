import streamlit as st
from database import criar_tabelas

st.set_page_config(
    page_title="Sistema Financeiro",
    page_icon="💰",
    layout="wide"
)

criar_tabelas()

if "logado" not in st.session_state:
    st.session_state["logado"] = False

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"


def mostrar_login():
    st.title("Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario == "admin" and senha == "123":
            st.session_state["logado"] = True
            st.session_state["pagina"] = "Dashboard"
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")


def mostrar_registro():
    st.title("Criar Conta")

    user = st.text_input("Novo usuário")
    pwd = st.text_input("Senha", type="password")

    if st.button("Registrar"):
        st.success("Conta criada!")
        st.session_state["pagina"] = "login"
        st.rerun()


def mostrar_area_logada():
    st.sidebar.title(f"Bem-vindo, {st.session_state['usuario'] if 'usuario' in st.session_state else ''}")

    escolha = st.sidebar.radio(
        "Menu",
        ["Dashboard", "Despesas", "Entradas", "Configurações", "Logout"]
    )

    if escolha == "Dashboard":
        st.title("📊 Dashboard")
        st.write("Conteúdo da Dashboard.")

    elif escolha == "Despesas":
        st.title("💸 Despesas")
        st.write("Listagem de despesas aqui.")

    elif escolha == "Entradas":
        st.title("💰 Entradas")
        st.write("Listagem de entradas aqui.")

    elif escolha == "Configurações":
        st.title("⚙️ Configurações")
        st.write("Preferências do sistema.")

    elif escolha == "Logout":
        st.session_state["logado"] = False
        st.session_state["pagina"] = "login"
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
