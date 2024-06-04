import tkinter as tk
import sqlite3
from database import criar_tabelas
from login_page import LoginPage

LOG_FILE_PATH = "log_acesso.txt"

if __name__ == "__main__":
    conn = sqlite3.connect('estoque.sqlite')
    criar_tabelas(conn)

    root = tk.Tk()
    login_page = LoginPage(root, conn, LOG_FILE_PATH)
    root.mainloop()
