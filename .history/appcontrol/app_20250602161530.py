import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Funções de manipulação de dados

def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            return json.load(f)
    return []

def salvar_dados(arquivo, dados):
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

def adicionar_pedido():
    pedido = {
        "produto": entry_produto.get(),
        "motoboy": entry_motoboy.get(),
        "tipo": combo_tipo.get(),
        "data": entry_data.get()
    }
    pedidos = carregar_dados("pedidos.json")
    pedidos.append(pedido)
    salvar_dados("pedidos.json", pedidos)
    messagebox.showinfo("Sucesso", "Pedido adicionado com sucesso!")
    entry_produto.delete(0, tk.END)
    entry_motoboy.delete(0, tk.END)
    entry_data.delete(0, tk.END)

# Funções de relatório/exportação

def exportar_pedidos_excel():
    pedidos = carregar_dados("pedidos.json")
    if not pedidos:
        messagebox.showinfo("Aviso", "Nenhum pedido cadastrado.")
        return
    df = pd.DataFrame(pedidos)
    df.to_excel("relatorio_pedidos.xlsx", index=False)
    messagebox.showinfo("Exportado", "Pedidos exportados para relatorio_pedidos.xlsx")

def gerar_relatorio():
    pedidos = carregar_dados("pedidos.json")
    if not pedidos:
        messagebox.showinfo("Aviso", "Nenhum pedido cadastrado.")
        return
    df = pd.DataFrame(pedidos)
    resumo = df.groupby(["motoboy", "tipo"]).size().unstack(fill_value=0)
    messagebox.showinfo("Relatório", resumo.to_string())

# Gráficos

def gerar_grafico_motoboy():
    pedidos = carregar_dados("pedidos.json")
    if not pedidos:
        messagebox.showinfo("Aviso", "Nenhum pedido cadastrado.")
        return

    df = pd.DataFrame(pedidos)
    contagem = df['motoboy'].value_counts()
    contagem.plot(kind='bar', title="Pedidos por Motoboy", color='skyblue')
    plt.ylabel("Quantidade de Pedidos")
    plt.xlabel("Motoboy")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def gerar_grafico_tipo():
    pedidos = carregar_dados("pedidos.json")
    if not pedidos:
        messagebox.showinfo("Aviso", "Nenhum pedido cadastrado.")
        return

    df = pd.DataFrame(pedidos)
    contagem = df['tipo'].value_counts()
    contagem.plot(kind='pie', autopct='%1.1f%%', startangle=90, title="Tipos de Pedido", ylabel="")
    plt.tight_layout()
    plt.show()

def gerar_grafico_dia_semana():
    pedidos = carregar_dados("pedidos.json")
    if not pedidos:
        messagebox.showinfo("Aviso", "Nenhum pedido cadastrado.")
        return

    df = pd.DataFrame(pedidos)
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df['dia_semana'] = df['data'].dt.day_name()

    contagem = df['dia_semana'].value_counts().reindex([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]).dropna()

    contagem.plot(kind='bar', title="Pedidos por Dia da Semana", color='orange')
    plt.ylabel("Quantidade de Pedidos")
    plt.xlabel("Dia da Semana")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Interface gráfica

root = tk.Tk()
root.title("Controle de Vendas")

frame_form = ttk.Frame(root)
frame_form.pack(pady=10)

# Entradas
entry_produto = ttk.Entry(frame_form, width=30)
entry_motoboy = ttk.Entry(frame_form, width=30)
entry_data = ttk.Entry(frame_form, width=30)
combo_tipo = ttk.Combobox(frame_form, values=["entrega", "retirada"], width=28)
combo_tipo.current(0)

entry_produto.grid(row=0, column=1, padx=5, pady=5)
entry_motoboy.grid(row=1, column=1, padx=5, pady=5)
combo_tipo.grid(row=2, column=1, padx=5, pady=5)
entry_data.grid(row=3, column=1, padx=5, pady=5)

# Labels
labels = ["Produto", "Motoboy", "Tipo de Pedido", "Data (AAAA-MM-DD)"]
for i, label in enumerate(labels):
    ttk.Label(frame_form, text=label).grid(row=i, column=0, sticky=tk.W)

# Botões
frame_botoes = ttk.Frame(root)
frame_botoes.pack(pady=10)

ttk.Button(frame_botoes, text="Adicionar Pedido", command=adicionar_pedido).grid(row=0, column=0, padx=5)
ttk.Button(frame_botoes, text="Gerar Relatório", command=gerar_relatorio).grid(row=0, column=1, padx=5)
ttk.Button(frame_botoes, text="Exportar para Excel", command=exportar_pedidos_excel).grid(row=0, column=2, padx=5)

ttk.Button(frame_botoes, text="Gráfico: Motoboy", command=gerar_grafico_motoboy).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(frame_botoes, text="Gráfico: Tipo", command=gerar_grafico_tipo).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(frame_botoes, text="Gráfico: Dia da Semana", command=gerar_grafico_dia_semana).grid(row=1, column=2, padx=5, pady=5)

root.mainloop()