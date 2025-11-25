# database.py
import sqlite3
import os
import hashlib

# Caminho absoluto do banco
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


# ---------------------------------------
# 🔌 Conexão
# ---------------------------------------
def conectar():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# ---------------------------------------
# 🏗️ Criação de tabelas
# ---------------------------------------
def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()

    # Usuários
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            senha TEXT
        )
    """)

    # Despesas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            descricao TEXT,
            valor REAL,
            categoria TEXT,
            data TEXT
        )
    """)

    # Entradas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS entradas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            descricao TEXT,
            valor REAL,
            categoria TEXT,
            data TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------
# 🔒 Usuários
# ---------------------------------------
def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def registrar_usuario(usuario, senha):
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
                    (usuario, hash_senha(senha)))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Erro ao registrar usuário:", e)
        return False


def autenticar_usuario(usuario, senha):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT senha FROM usuarios WHERE usuario=?", (usuario,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return False

    return row[0] == hash_senha(senha)


# ---------------------------------------
# 💸 DESPESAS
# ---------------------------------------
def listar_despesas(usuario):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, descricao, valor, categoria, data
        FROM despesas
        WHERE usuario=?
        ORDER BY date(data) DESC, id DESC
    """, (usuario,))
    dados = cur.fetchall()
    conn.close()
    return dados


def adicionar_despesa(usuario, descricao, valor, categoria, data):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO despesas (usuario, descricao, valor, categoria, data)
        VALUES (?, ?, ?, ?, ?)
    """, (usuario, descricao, valor, categoria, data))
    conn.commit()
    conn.close()


def editar_despesa(id_, descricao, valor, categoria, data):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        UPDATE despesas
        SET descricao=?, valor=?, categoria=?, data=?
        WHERE id=?
    """, (descricao, valor, categoria, data, id_))
    conn.commit()
    conn.close()


def excluir_despesa(id_):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM despesas WHERE id=?", (id_,))
    conn.commit()
    conn.close()


# ---------------------------------------
# 💰 ENTRADAS
# ---------------------------------------
def listar_entradas(usuario):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, descricao, valor, categoria, data
        FROM entradas
        WHERE usuario=?
        ORDER BY date(data) DESC, id DESC
    """, (usuario,))
    dados = cur.fetchall()
    conn.close()
    return dados


def adicionar_entrada(usuario, descricao, valor, categoria, data):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO entradas (usuario, descricao, valor, categoria, data)
        VALUES (?, ?, ?, ?, ?)
    """, (usuario, descricao, valor, categoria, data))
    conn.commit()
    conn.close()


def editar_entrada(id_, descricao, valor, categoria, data):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        UPDATE entradas
        SET descricao=?, valor=?, categoria=?, data=?
        WHERE id=?
    """, (descricao, valor, categoria, data, id_))
    conn.commit()
    conn.close()


def excluir_entrada(id_):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM entradas WHERE id=?", (id_,))
    conn.commit()
    conn.close()
