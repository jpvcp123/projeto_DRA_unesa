import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class CadastroPage:
    def __init__(self, root, conn, log_file_path):
        self.root = root
        self.conn = conn
        self.c = self.conn.cursor()
        self.log_file_path = log_file_path

        self.root.title("Cadastro")
        self.root.geometry("400x200")

        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=20)

        self.lbl_username = ttk.Label(self.frame, text="Novo Usuário:")
        self.lbl_username.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_username = ttk.Entry(self.frame)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_password = ttk.Label(self.frame, text="Nova Senha:")
        self.lbl_password.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_password = ttk.Entry(self.frame, show='*')
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.btn_cadastrar = ttk.Button(self.frame, text="Cadastrar", command=self.cadastrar)
        self.btn_cadastrar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def cadastrar(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username and password:
            try:
                self.c.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
                self.conn.commit()
                self.write_log(f"Novo usuário cadastrado: {username}")
                messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
                self.root.destroy()
                root = tk.Tk()
                from login_page import LoginPage 
                login_page = LoginPage(root, self.conn, self.log_file_path)
                root.mainloop()
            except sqlite3.Error as e:
                messagebox.showwarning("Erro", str(e))
        else:
            messagebox.showwarning("Cadastro", "Por favor, preencha todos os campos!")

    def write_log(self, message):
        with open(self.log_file_path, "a") as log_file:
            log_file.write(f"{datetime.now()} - {message}\n")
