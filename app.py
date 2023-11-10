import tkinter as tk
from tkinter import ttk
from datetime import date, datetime
import re
import csv
from tkcalendar import DateEntry

def adicionar_boleto(event=None):
    data_insercao = date.today()
    empresa = empresa_entry.get().capitalize()
    vencimento = vencimento_entry.get_date().strftime('%d/%m/%Y')
    valor = valor_entry.get()
    
    # Verifica se os campos de nome, data de vencimento e valor estão preenchidos
    if not empresa or not vencimento or not valor:
        resultado_label.config(text="Preencha todos os campos antes de adicionar um boleto")
        return
    
    # Verifica se o valor inserido é um número válido com no máximo 2 casas decimais e sem letras
    valor = valor.replace(',', '.')  # Substitui vírgulas por pontos
    if is_valid_value(valor):
        valor = f"R$ {valor}"
        tree.insert('', 'end', values=(data_insercao.strftime('%d/%m/%Y'), empresa, vencimento, valor))
        salvar_boletos()  # Salva os boletos no arquivo
        resultado_label.config(text="")
        # Limpar os campos de entrada
        empresa_entry.delete(0, 'end')
        vencimento_entry.set_date(date.today())
        valor_entry.delete(0, 'end')
        empresa_entry.focus()  # Move o foco para o campo "Nome da Empresa"
    else:
        resultado_label.config(text="Valor inválido. Insira um valor numérico válido.")

def apenas_numeros(event):
    entrada = event.widget.get()
    entrada = entrada.replace(',', '.')  # Substitui vírgulas por pontos
    if not entrada.replace('.', '', 1).isdigit():
        event.widget.delete(0, tk.END)  # Limpa o campo se houver caracteres inválidos

# Função para excluir um boleto selecionado
def excluir_boleto():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)

# Função para salvar os boletos em um arquivo CSV
def salvar_boletos():
    with open("boletos.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Data de Inserção", "Nome da Empresa", "Data de Vencimento", "Valor"])
        for item in tree.get_children():
            values = tree.item(item, 'values')
            writer.writerow(values)
        data = [(tree.item(item, 'values')[2], item) for item in tree.get_children()]
    data.sort(key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'))
    for index, (_, item) in enumerate(data):
        tree.move(item, '', index)

# Função para pesquisar boletos por nome da empresa
def pesquisar_boleto(event=None):
    search_text = data_pesquisa_entry.get().strip()
    if search_text:
        items = tree.get_children()
        for item in items:
            values = tree.item(item, 'values')
            if values[1].lower() == search_text.lower():
                tree.selection_set(item)
                tree.focus(item)
                return
        # Se não encontrado, exibir mensagem
        resultado_label.config(text="Boleto não encontrado")
    else:
        resultado_label.config(text="")

# Função para verificar se a entrada é um número válido com no máximo 2 casas decimais
def is_valid_value(value):
    try:
        float(value)
        if re.match(r'^\d+(\.\d{1,2})?$', value):
            return True
        else:
            return False
    except ValueError:
        return False
    
    
# Configuração da janela principal
root = tk.Tk()
root.title("Sistema de Gerenciamento de Boletos")

empresa_label = tk.Label(root, text="Nome:")
empresa_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
empresa_label.columnconfigure(0, weight=1, minsize=100)

empresa_entry = tk.Entry(root)
empresa_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
empresa_entry.columnconfigure(0, weight=2, minsize=50)

empresa_entry.focus()  # Move o foco para o campo "Nome da Empresa"

vencimento_label = tk.Label(root, text="Data de Vencimento:")
vencimento_label.grid(row=0, column=2, padx=5, pady=5, sticky='w')

vencimento_entry = DateEntry(root, date_pattern='dd/mm/yyyy')
vencimento_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')


valor_label = tk.Label(root, text="Valor:")
valor_label.grid(row=0, column=4, padx=5, pady=5, sticky='w')

valor_entry = tk.Entry(root)
valor_entry.grid(row=0, column=5, padx=5, pady=5, sticky='w')
valor_entry.bind('<KeyRelease>', apenas_numeros)

# Associa o evento "Enter" ao campo de valor
valor_entry.bind('<Return>', adicionar_boleto)

adicionar_button = tk.Button(root, text="Adicionar Boleto", command=adicionar_boleto)
adicionar_button.grid(row=0, column=6, padx=5, pady=5, sticky='w')

data_pesquisa_label = tk.Label(root, text="Pesquisar por Nome da Empresa:")
data_pesquisa_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
data_pesquisa_entry = tk.Entry(root)
data_pesquisa_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

# Associa o evento "Enter" ao campo de pesquisa
data_pesquisa_entry.bind('<Return>', pesquisar_boleto)

pesquisar_button = tk.Button(root, text="Pesquisar", command=pesquisar_boleto)
pesquisar_button.grid(row=1, column=2, padx=5, pady=5, sticky='w')

resultado_label = tk.Label(root, text="")
resultado_label.grid(row=1, column=3, padx=5, pady=5, sticky='w')

excluir_button = tk.Button(root, text="Excluir Boleto", command=excluir_boleto)
excluir_button.grid(row=3, columnspan=6, padx=5, pady=5, sticky='w')

# Criação da tabela para exibir os boletos
tree = ttk.Treeview(root, columns=("Data de Inserção", "Empresa", "Data de Vencimento", "Valor"), show="headings")
tree.heading("Data de Inserção", text="Data de Inserção")
tree.heading("Empresa", text="Nome da Empresa")
tree.heading("Data de Vencimento", text="Data de Vencimento")
tree.heading("Valor", text="Valor")
tree.grid(row=4, columnspan=7, sticky='nsew')

tree.column("Data de Inserção", width=120, anchor="center")  # Ajuste de formatação

# Iniciar a interface gráfica
root.mainloop()
