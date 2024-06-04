import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class LoginPage:
    def __init__(self, root, conn, log_file_path):
        self.root = root
        self.conn = conn
        self.c = self.conn.cursor()
        self.log_file_path = log_file_path

        self.root.title("Login")
        self.root.geometry("400x200")

        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=20)

        self.lbl_username = ttk.Label(self.frame, text="Usuário:")
        self.lbl_username.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_username = ttk.Entry(self.frame)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_password = ttk.Label(self.frame, text="Senha:")
        self.lbl_password.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_password = ttk.Entry(self.frame, show='*')
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.btn_login = ttk.Button(self.frame, text="Login", command=self.login)
        self.btn_login.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.btn_cadastrar = ttk.Button(self.frame, text="Cadastrar", command=self.abrir_tela_cadastro)
        self.btn_cadastrar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        self.c.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
        user = self.c.fetchone()

        if user:
            self.write_log(f"Usuário {username} logado com sucesso")
            self.root.destroy()
            root = tk.Tk()
            from estoque_app import EstoqueApp 
            app = EstoqueApp(root, self.conn)
            root.mainloop()
        else:
            self.write_log(f"Tentativa de login falhada para o usuário {username}")
            messagebox.showwarning("Login", "Usuário ou senha incorretos!")

    def abrir_tela_cadastro(self):
        self.root.destroy()
        root = tk.Tk()
        from cadastro_page import CadastroPage 
        cadastro_page = CadastroPage(root, self.conn, self.log_file_path)
        root.mainloop()

    def write_log(self, message):
        with open(self.log_file_path, "a") as log_file:
            log_file.write(f"{datetime.now()} - {message}\n")
