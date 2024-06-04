import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class EstoqueApp:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.c = self.conn.cursor()

        self.root.title("Estoque de Produtos")

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#F5F5DC')  
        self.style.configure('TButton', background='#CD5C5C', foreground='white')  
        self.style.configure('TLabel', background='#F5F5DC')  
        self.style.configure('TEntry', background='#FFF')
        self.style.configure('Treeview', background='#FFF')

        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=20)

        self.lbl_id = ttk.Label(self.frame, text="ID:")
        self.lbl_id.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_id = ttk.Entry(self.frame)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_produto = ttk.Label(self.frame, text="Produto:")
        self.lbl_produto.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_produto = ttk.Entry(self.frame)
        self.entry_produto.grid(row=1, column=1, padx=5, pady=5)

        self.lbl_valor = ttk.Label(self.frame, text="Valor:")
        self.lbl_valor.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_valor = ttk.Entry(self.frame)
        self.entry_valor.grid(row=2, column=1, padx=5, pady=5)

        self.btn_adicionar = ttk.Button(self.frame, text="Adicionar", command=self.adicionar_produto)
        self.btn_adicionar.grid(row=0, column=2, padx=5, pady=5)

        self.btn_editar = ttk.Button(self.frame, text="Editar", command=self.abrir_tela_edicao)
        self.btn_editar.grid(row=1, column=2, padx=5, pady=5)

        self.btn_excluir = ttk.Button(self.frame, text="Excluir", command=self.excluir_produto)
        self.btn_excluir.grid(row=2, column=2, padx=5, pady=5)

        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(pady=20)

        self.table = ttk.Treeview(self.table_frame, columns=('id', 'produto', 'valor'), show='headings', selectmode='browse')
        self.table.column('id', width=100)
        self.table.column('produto', width=200)
        self.table.column('valor', width=100)
        self.table.heading('id', text='ID')
        self.table.heading('produto', text='Produto')
        self.table.heading('valor', text='Valor')
        self.table.pack(side='left', fill='both')

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.table.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.table.configure(yscrollcommand=self.scrollbar.set)

        self.carregar_produtos()

    def adicionar_produto(self):
        id = self.entry_id.get()
        produto = self.entry_produto.get()
        valor = self.entry_valor.get()

        if id and produto and valor:
            try:
                self.c.execute("INSERT INTO produto (id, produto, valor) VALUES (?, ?, ?)", (id, produto, valor))
                self.conn.commit()
                messagebox.showinfo("Adicionar Produto", "Produto adicionado com sucesso!")
                self.entry_id.delete(0, tk.END)
                self.entry_produto.delete(0, tk.END)
                self.entry_valor.delete(0, tk.END)
                self.carregar_produtos()
            except sqlite3.Error as e:
                messagebox.showwarning("Erro", str(e))
        else:
            messagebox.showwarning("Adicionar Produto", "Por favor, preencha todos os campos!")

    def excluir_produto(self):
        selected_item = self.table.selection()
        if selected_item:
            item = self.table.item(selected_item)
            id = item['values'][0]
            try:
                self.c.execute("DELETE FROM produto WHERE id=?", (id,))
                self.conn.commit()
                messagebox.showinfo("Excluir Produto", "Produto excluído com sucesso!")
                self.carregar_produtos()
            except sqlite3.Error as e:
                messagebox.showwarning("Erro", str(e))
        else:
            messagebox.showwarning("Excluir Produto", "Por favor, selecione um produto!")

    def carregar_produtos(self):
        for row in self.table.get_children():
            self.table.delete(row)
        self.c.execute("SELECT * FROM produto")
        for row in self.c.fetchall():
            self.table.insert('', 'end', values=row)

    def abrir_tela_edicao(self):
        selected_item = self.table.selection()
        if selected_item:
            item = self.table.item(selected_item)
            id = item['values'][0]

            edit_window = tk.Toplevel(self.root)
            edit_window.title("Editar Produto")

            frame = ttk.Frame(edit_window)
            frame.pack(pady=20)

            lbl_id = ttk.Label(frame, text="ID:")
            lbl_id.grid(row=0, column=0, padx=5, pady=5, sticky='e')
            entry_id = ttk.Entry(frame)
            entry_id.grid(row=0, column=1, padx=5, pady=5)
            entry_id.insert(0, item['values'][0])
            entry_id.config(state='disabled')

            lbl_produto = ttk.Label(frame, text="Produto:")
            lbl_produto.grid(row=1, column=0, padx=5, pady=5, sticky='e')
            entry_produto = ttk.Entry(frame)
            entry_produto.grid(row=1, column=1, padx=5, pady=5)
            entry_produto.insert(0, item['values'][1])

            lbl_valor = ttk.Label(frame, text="Valor:")
            lbl_valor.grid(row=2, column=0, padx=5, pady=5, sticky='e')
            entry_valor = ttk.Entry(frame)
            entry_valor.grid(row=2, column=1, padx=5, pady=5)
            entry_valor.insert(0, item['values'][2])

            def salvar_edicao():
                produto = entry_produto.get()
                valor = entry_valor.get()
                try:
                    self.c.execute("UPDATE produto SET produto=?, valor=? WHERE id=?", (produto, valor, id))
                    self.conn.commit()
                    messagebox.showinfo("Editar Produto", "Produto editado com sucesso!")
                    edit_window.destroy()
                    self.carregar_produtos()
                except sqlite3.Error as e:
                    messagebox.showwarning("Erro", str(e))

            btn_salvar = ttk.Button(frame, text="Salvar", command=salvar_edicao)
            btn_salvar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        else:
            messagebox.showwarning("Editar Produto", "Por favor, selecione um produto!")
