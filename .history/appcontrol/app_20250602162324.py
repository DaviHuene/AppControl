import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Funções auxiliares
def carregar_dados(nome_arquivo):
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r') as f:
            return json.load(f)
    return []

def salvar_dados(nome_arquivo, dados):
    with open(nome_arquivo, 'w') as f:
        json.dump(dados, f, indent=4)

# Caminhos dos arquivos
ARQ_PRODUTOS = 'produtos.json'
ARQ_MOTOBOYS = 'motoboys.json'
ARQ_PEDIDOS = 'pedidos.json'

# Carregar dados
produtos = carregar_dados(ARQ_PRODUTOS)
motoboys = carregar_dados(ARQ_MOTOBOYS)
pedidos = carregar_dados(ARQ_PEDIDOS)

# Funções principais
def adicionar_produto():
    nome = simpledialog.askstring("Produto", "Nome do produto:")
    preco = simpledialog.askfloat("Produto", "Preço do produto:")
    if nome and preco is not None:
        produtos.append({"nome": nome, "preco": preco})
        salvar_dados(ARQ_PRODUTOS, produtos)
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")

def adicionar_motoboy():
    nome = simpledialog.askstring("Motoboy", "Nome do motoboy:")
    if nome:
        motoboys.append({"nome": nome})
        salvar_dados(ARQ_MOTOBOYS, motoboys)
        messagebox.showinfo("Sucesso", "Motoboy adicionado com sucesso!")

def fazer_pedido():
    if not produtos or not motoboys:
        messagebox.showwarning("Atenção", "Cadastre produtos e motoboys primeiro.")
        return

    def confirmar_pedido():
        nome_cliente = entry_cliente.get()
        produto = combo_produto.get()
        motoboy = combo_motoboy.get()
        tipo = combo_tipo.get()

        if not all([nome_cliente, produto, motoboy, tipo]):
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        valor = next(p["preco"] for p in produtos if p["nome"] == produto)
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        pedidos.append({
            "cliente": nome_cliente,
            "produto": produto,
            "valor": valor,
            "motoboy": motoboy,
            "tipo": tipo,
            "data": data_hora
        })

        salvar_dados(ARQ_PEDIDOS, pedidos)
        messagebox.showinfo("Sucesso", "Pedido registrado!")
        janela.destroy()

    janela = tk.Toplevel(root)
    janela.title("Novo Pedido")

    tk.Label(janela, text="Cliente:").pack()
    entry_cliente = tk.Entry(janela)
    entry_cliente.pack()

    tk.Label(janela, text="Produto:").pack()
    combo_produto = ttk.Combobox(janela, values=[p["nome"] for p in produtos])
    combo_produto.pack()

    tk.Label(janela, text="Motoboy:").pack()
    combo_motoboy = ttk.Combobox(janela, values=[m["nome"] for m in motoboys])
    combo_motoboy.pack()

    tk.Label(janela, text="Tipo de pedido:").pack()
    combo_tipo = ttk.Combobox(janela, values=["Retirada", "Entrega"])
    combo_tipo.pack()

    tk.Button(janela, text="Confirmar", command=confirmar_pedido).pack(pady=10)

def exportar_pedidos_excel():
    if not pedidos:
        messagebox.showwarning("Aviso", "Nenhum pedido registrado.")
        return
    df = pd.DataFrame(pedidos)
    caminho = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if caminho:
        df.to_excel(caminho, index=False)
        messagebox.showinfo("Sucesso", "Pedidos exportados com sucesso!")

def gerar_relatorio():
    if not pedidos:
        messagebox.showwarning("Aviso", "Nenhum pedido registrado.")
        return
    df = pd.DataFrame(pedidos)
    relatorio = df.groupby(['motoboy', 'tipo']).size().unstack(fill_value=0)
    messagebox.showinfo("Relatório", relatorio.to_string())

def gerar_graficos():
    if not pedidos:
        messagebox.showwarning("Aviso", "Nenhum pedido registrado.")
        return

    df = pd.DataFrame(pedidos)
    df["data"] = pd.to_datetime(df["data"])

    fig, axs = plt.subplots(3, 1, figsize=(8, 12))
    fig.suptitle("Relatórios Visuais", fontsize=16)

    # Gráfico de pedidos por motoboy
    df['motoboy'].value_counts().plot(kind='bar', ax=axs[0], color='skyblue')
    axs[0].set_title("Pedidos por Motoboy")
    axs[0].set_ylabel("Quantidade")

    # Gráfico de tipo de pedido
    df['tipo'].value_counts().plot(kind='pie', ax=axs[1], autopct='%1.1f%%', startangle=90)
    axs[1].set_title("Tipos de Pedido")
    axs[1].axis('equal')

    # Gráfico de pedidos por dia da semana
    df['dia'] = df['data'].dt.day_name()
    df['dia'].value_counts().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ]).plot(kind='bar', ax=axs[2], color='orange')
    axs[2].set_title("Pedidos por Dia da Semana")
    axs[2].set_ylabel("Quantidade")

    plt.tight_layout()
    plt.show()

# Interface principal
root = tk.Tk()
root.title("Controle de Vendas")

ttk.Button(root, text="Adicionar Produto", command=adicionar_produto).pack(pady=5)
ttk.Button(root, text="Adicionar Motoboy", command=adicionar_motoboy).pack(pady=5)
ttk.Button(root, text="Fazer Pedido", command=fazer_pedido).pack(pady=5)

ttk.Separator(root, orient="horizontal").pack(fill="x", pady=10)

ttk.Button(root, text="Exportar Pedidos para Excel", command=exportar_pedidos_excel).pack(pady=5)
ttk.Button(root, text="Gerar Relatório", command=gerar_relatorio).pack(pady=5)
ttk.Button(root, text="Mostrar Gráficos", command=gerar_graficos).pack(pady=5)

root.mainloop()
