import sqlite3

def criar_tabelas(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS produto (
                    id TEXT PRIMARY KEY,
                    produto TEXT,
                    valor REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    username TEXT PRIMARY KEY,
                    password TEXT)''')
    conn.commit()
