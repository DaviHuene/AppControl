""import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ControleVendasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Vendas")

        self.produtos = self.carregar_dados("produtos.json")
        self.motoboys = self.carregar_dados("motoboys.json")
        self.pedidos = self.carregar_dados("pedidos.json")

        self.criar_widgets()

    def carregar_dados(self, arquivo):
        if os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def salvar_dados(self, dados, arquivo):
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def criar_widgets(self):
        self.tabs = ttk.Notebook(self.root)

        self.tab_produtos = ttk.Frame(self.tabs)
        self.tab_motoboys = ttk.Frame(self.tabs)
        self.tab_pedidos = ttk.Frame(self.tabs)
        self.tab_exportacao = ttk.Frame(self.tabs)
        self.tab_relatorios = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_produtos, text="Produtos")
        self.tabs.add(self.tab_motoboys, text="Motoboys")
        self.tabs.add(self.tab_pedidos, text="Pedidos")
        self.tabs.add(self.tab_exportacao, text="Exportação")
        self.tabs.add(self.tab_relatorios, text="Relatórios")
        self.tabs.pack(expand=1, fill="both")

        # Produtos
        self.lista_produtos = tk.Listbox(self.tab_produtos)
        self.lista_produtos.pack(side="left", fill="both", expand=True)
        self.atualizar_lista(self.lista_produtos, self.produtos)

        frame_produtos = tk.Frame(self.tab_produtos)
        frame_produtos.pack(side="right", fill="y")
        tk.Button(frame_produtos, text="Adicionar Produto", command=self.adicionar_produto).pack(fill="x")
        tk.Button(frame_produtos, text="Remover Produto", command=self.remover_produto).pack(fill="x")

        # Motoboys
        self.lista_motoboys = tk.Listbox(self.tab_motoboys)
        self.lista_motoboys.pack(side="left", fill="both", expand=True)
        self.atualizar_lista(self.lista_motoboys, self.motoboys)

        frame_motoboys = tk.Frame(self.tab_motoboys)
        frame_motoboys.pack(side="right", fill="y")
        tk.Button(frame_motoboys, text="Adicionar Motoboy", command=self.adicionar_motoboy).pack(fill="x")
        tk.Button(frame_motoboys, text="Remover Motoboy", command=self.remover_motoboy).pack(fill="x")

        # Pedidos
        self.lista_pedidos = tk.Listbox(self.tab_pedidos)
        self.lista_pedidos.pack(side="left", fill="both", expand=True)
        self.atualizar_lista(self.lista_pedidos, self.pedidos)

        frame_pedidos = tk.Frame(self.tab_pedidos)
        frame_pedidos.pack(side="right", fill="y")
        tk.Button(frame_pedidos, text="Adicionar Pedido", command=self.adicionar_pedido).pack(fill="x")

        # Exportação
        frame_exportacao = tk.Frame(self.tab_exportacao)
        frame_exportacao.pack(fill="both", expand=True)
        tk.Button(frame_exportacao, text="Exportar para Excel", command=self.exportar_excel).pack(fill="x")
        self.lista_exportacao = tk.Listbox(self.tab_exportacao)
        self.lista_exportacao.pack(fill="both", expand=True)
        self.atualizar_lista(self.lista_exportacao, self.pedidos)

        # Relatórios
        frame_relatorios = tk.Frame(self.tab_relatorios)
        frame_relatorios.pack(fill="both", expand=False)
        tk.Button(frame_relatorios, text="Gerar por Período", command=self.relatorio_por_periodo).pack(fill="x")
        tk.Button(frame_relatorios, text="Gerar por Motoboy", command=self.relatorio_por_motoboy).pack(fill="x")
        tk.Button(frame_relatorios, text="Gerar por Tipo de Pedido", command=self.relatorio_por_tipo).pack(fill="x")

        self.canvas_frame = tk.Frame(self.tab_relatorios)
        self.canvas_frame.pack(fill="both", expand=True)

    def atualizar_lista(self, lista, dados):
        lista.delete(0, tk.END)
        for item in dados:
            lista.insert(tk.END, item)

    def adicionar_produto(self):
        produto = simpledialog.askstring("Produto", "Nome do Produto:")
        if produto:
            self.produtos.append(produto)
            self.salvar_dados(self.produtos, "produtos.json")
            self.atualizar_lista(self.lista_produtos, self.produtos)

    def remover_produto(self):
        sel = self.lista_produtos.curselection()
        if sel:
            del self.produtos[sel[0]]
            self.salvar_dados(self.produtos, "produtos.json")
            self.atualizar_lista(self.lista_produtos, self.produtos)

    def adicionar_motoboy(self):
        nome = simpledialog.askstring("Motoboy", "Nome do Motoboy:")
        if nome:
            self.motoboys.append(nome)
            self.salvar_dados(self.motoboys, "motoboys.json")
            self.atualizar_lista(self.lista_motoboys, self.motoboys)

    def remover_motoboy(self):
        sel = self.lista_motoboys.curselection()
        if sel:
            del self.motoboys[sel[0]]
            self.salvar_dados(self.motoboys, "motoboys.json")
            self.atualizar_lista(self.lista_motoboys, self.motoboys)

    def adicionar_pedido(self):
        if not self.produtos or not self.motoboys:
            messagebox.showerror("Erro", "Cadastre produtos e motoboys antes de adicionar um pedido.")
            return

        produto = simpledialog.askstring("Pedido", f"Produto ({', '.join(self.produtos)}):")
        if produto not in self.produtos:
            messagebox.showerror("Erro", "Produto inválido.")
            return

        motoboy = simpledialog.askstring("Pedido", f"Motoboy ({', '.join(self.motoboys)}):")
        if motoboy not in self.motoboys:
            messagebox.showerror("Erro", "Motoboy inválido.")
            return

        tipo = simpledialog.askstring("Tipo de Pedido", "Tipo de Pedido (Delivery, Retirada, etc):")
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pedido = f"{data} | {produto} | {motoboy} | {tipo}"
        self.pedidos.append(pedido)
        self.salvar_dados(self.pedidos, "pedidos.json")
        self.atualizar_lista(self.lista_pedidos, self.pedidos)
        self.atualizar_lista(self.lista_exportacao, self.pedidos)

    def exportar_excel(self):
        if not self.pedidos:
            messagebox.showwarning("Atenção", "Nenhum pedido para exportar.")
            return
        df = pd.DataFrame([p.split(" | ") for p in self.pedidos], columns=["Data", "Produto", "Motoboy", "Tipo"])
        df.to_excel("pedidos_exportados.xlsx", index=False)
        messagebox.showinfo("Exportado", "Pedidos exportados para pedidos_exportados.xlsx")

    def gerar_grafico(self, df, coluna, titulo):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        contagem = df[coluna].value_counts()
        fig, ax = plt.subplots()
        contagem.plot(kind='bar', ax=ax)
        ax.set_title(titulo)
        ax.set_ylabel("Quantidade")

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def relatorio_por_periodo(self):
        inicio = simpledialog.askstring("Início", "Data início (YYYY-MM-DD):")
        fim = simpledialog.askstring("Fim", "Data fim (YYYY-MM-DD):")
        try:
            df = pd.DataFrame([p.split(" | ") for p in self.pedidos], columns=["Data", "Produto", "Motoboy", "Tipo"])
            df['Data'] = pd.to_datetime(df['Data'])
            df_filtrado = df[(df['Data'] >= inicio) & (df['Data'] <= fim)]
            self.gerar_grafico(df_filtrado, 'Produto', f"Pedidos por Produto de {inicio} a {fim}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")

    def relatorio_por_motoboy(self):
        df = pd.DataFrame([p.split(" | ") for p in self.pedidos], columns=["Data", "Produto", "Motoboy", "Tipo"])
        self.gerar_grafico(df, 'Motoboy', "Pedidos por Motoboy")

    def relatorio_por_tipo(self):
        df = pd.DataFrame([p.split(" | ") for p in self.pedidos], columns=["Data", "Produto", "Motoboy", "Tipo"])
        self.gerar_grafico(df, 'Tipo', "Pedidos por Tipo de Entrega")

if __name__ == "__main__":
    root = tk.Tk()
    app = ControleVendasApp(root)
    root.mainloop()
