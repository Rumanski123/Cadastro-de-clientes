import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Conexão e criação de tabela
def conectar():
    return sqlite3.connect('empresas.db')

def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cnpj TEXT NOT NULL UNIQUE,
            razao_social TEXT NOT NULL,
            endereco TEXT,
            cep TEXT,
            telefone TEXT,
            email TEXT,
            observacoes TEXT,
            data_prospeccao TEXT,
            data_visita TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Inserir dados
def inserir_empresa():
    dados = (
        entrada_cnpj.get(),
        entrada_razao.get(),
        entrada_endereco.get(),
        entrada_cep.get(),
        entrada_telefone.get(),
        entrada_email.get(),
        entrada_obs.get(),
        entrada_prospeccao.get(),
        entrada_visita.get()
    )

    if all(dados[:2]):  
        try:
            conn = conectar()
            c = conn.cursor()
            c.execute('''
                INSERT INTO empresas (
                    cnpj, razao_social, endereco, cep, telefone, email, observacoes, data_prospeccao, data_visita
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', dados)
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', 'Empresa cadastrada com sucesso!')
            limpar_campos()
            mostrar_empresas()
        except sqlite3.IntegrityError as e:
            print("Erro ao inserir:", e)
            messagebox.showerror('Erro', 'CNPJ já cadastrado.')
    else:
        messagebox.showwarning('Campos obrigatórios', 'Preencha pelo menos o CNPJ e Razão Social.')


def mostrar_empresas():
    for i in tree.get_children():
        tree.delete(i)

    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM empresas')
    for row in c.fetchall():
        tree.insert('', 'end', values=row)
    conn.close()


def deletar_empresa():
    selecionado = tree.selection()
    if selecionado:
        confirmacao = messagebox.askyesno("Confirmação", "Deseja realmente deletar esta empresa?")
        if confirmacao:
            empresa_id = tree.item(selecionado)['values'][0]
            conn = conectar()
            c = conn.cursor()
            c.execute('DELETE FROM empresas WHERE id = ?', (empresa_id,))
            conn.commit()
            conn.close()
            mostrar_empresas()
            limpar_campos()
    else:
        messagebox.showwarning('Seleção necessária', 'Selecione uma empresa para deletar.')


def editar_empresa():
    selecionado = tree.selection()
    if selecionado:
        empresa_id = tree.item(selecionado)['values'][0]
        dados = (
            entry_cnpj.get(),
            entry_razao.get(),
            entry_endereco.get(),
            entry_cep.get(),
            entry_telefone.get(),
            entry_email.get(),
            entry_obs.get(),
            entry_prospeccao.get(),
            entry_visita.get()
        )

        if dados[0] and dados[1]:  
            try:
                conn = conectar()
                c = conn.cursor()
                c.execute('''
                    UPDATE empresas SET
                        cnpj = ?, razao_social = ?, endereco = ?, cep = ?, telefone = ?, email = ?, observacoes = ?, data_prospeccao = ?, data_visita = ?
                    WHERE id = ?
                ''', (*dados, empresa_id))
                conn.commit()
                conn.close()
                mostrar_empresas()
                limpar_campos()
                messagebox.showinfo('Atualizado', 'Dados atualizados com sucesso!')
            except sqlite3.IntegrityError:
                messagebox.showerror('Erro', 'CNPJ já cadastrado por outra empresa.')
        else:
            messagebox.showwarning('Campos obrigatórios', 'Preencha CNPJ e Razão Social.')
    else:
        messagebox.showwarning('Seleção necessária', 'Selecione uma empresa para editar.')


def preencher_campos(event):
    selecionado = tree.selection()
    if selecionado:
        valores = tree.item(selecionado)['values']
        for entry, valor in zip(entries, valores[1:]):
            entry.delete(0, tk.END)
            entry.insert(0, valor)


def limpar_campos():
    for entry in entries:
        entry.delete(0, tk.END)


def bind_enter_navigation():
    for i in range(len(entries) - 1):
        entries[i].bind("<Return>", lambda e, next_entry=entries[i+1]: next_entry.focus_set())
    entries[-1].bind("<Return>", lambda e: inserir_empresa())


janela = tk.Tk()
janela.title("Cadastro de Empresas")
janela.geometry("1800x950")
janela.geometry("+80+30")
janela.resizable(False, False)
janela.configure(bg="#2C2C2C")  


style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#333333",
                foreground="white",
                fieldbackground="#333333",
                rowheight=25,
                font=('Arial', 10))
style.configure("Treeview.Heading",
                background="#444444",
                foreground="white",
                font=('Arial', 11, 'bold'))

frame_form = tk.Frame(janela, padx=20, pady=20, bg="#2C2C2C")
frame_form.pack()

labels = [
    "CNPJ", "Razão Social", "Endereço", "CEP", "Telefone",
    "E-mail", "Observações", "Data de Prospecção", "Data de Visita"
]

entries = []
for i, label in enumerate(labels):
    tk.Label(frame_form, text=label + ":", font=("Arial", 12), bg="#2C2C2C", fg="white").grid(row=i, column=0, sticky="e")
    entry = tk.Entry(frame_form, font=("Arial", 12), width=40, bg="#3C3F41", fg="white", insertbackground="white")
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

(entry_cnpj, entry_razao, entry_endereco, entry_cep,
 entry_telefone, entry_email, entry_obs, entry_prospeccao, entry_visita) = entries

bind_enter_navigation()


frame_botoes = tk.Frame(janela, pady=10, bg="#2C2C2C")
frame_botoes.pack()

tk.Button(frame_botoes, text="Salvar", command=inserir_empresa,
          width=15, bg="#4CAF50", fg="white", activebackground="#388E3C").grid(row=0, column=0, padx=5)

tk.Button(frame_botoes, text="Atualizar", command=editar_empresa,
          width=15, bg="#2196F3", fg="white", activebackground="#1976D2").grid(row=0, column=1, padx=5)

tk.Button(frame_botoes, text="Deletar", command=deletar_empresa,
          width=15, bg="#F44336", fg="white", activebackground="#C62828").grid(row=0, column=2, padx=5)

tk.Button(frame_botoes, text="Limpar", command=limpar_campos,
          width=15, bg="#777777", fg="white", activebackground="#999999").grid(row=0, column=3, padx=5)

# Tabela
frame_tabela = tk.Frame(janela, bg="#2C2C2C")
frame_tabela.pack(pady=10)

colunas = ("ID", "CNPJ", "Razão Social", "Endereço", "CEP", "Telefone", "E-mail", "Observações", "Data Prospecção", "Data Visita")
tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=12)

for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=160)

tree.bind("<<TreeviewSelect>>", preencher_campos)
tree.pack()


criar_tabela()
mostrar_empresas()
janela.mainloop()
