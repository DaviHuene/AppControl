import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

# Configurações de Cores
DARK_BG = '#121212'
DARK_FG = '#e0e0e0'
DARK_ENTRY = '#1e1e1e'
DARK_TREE = '#252525'
DARK_SELECTION = '#424242'

# Fontes
FONT = ('Segoe UI', 10)
FONT_BOLD = ('Segoe UI', 10, 'bold')

# Arquivos de dados
DADOS = {
    'produtos': 'produtos.json',
    'motoboys': 'motoboys.json',
    'pedidos': 'pedidos.json'
}

PERCENTUAL_IFOOD = 0.20

class DataManager:
    @staticmethod
    def carregar(arquivo):
        if not os.path.exists(arquivo):
            return []
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def salvar(arquivo, dados):
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Garagem do Frango - Controle")
        self.geometry("1000x700")
        self.configure(bg=DARK_BG)
        
        self._configurar_estilo()
        self._carregar_dados()
        self._criar_interface()

    def _configurar_estilo(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        
        style.configure('.', background=DARK_BG, foreground=DARK_FG, font=FONT)
        style.configure('TFrame', background=DARK_BG)
        style.configure('TLabel', background=DARK_BG, foreground=DARK_FG)
        style.configure('TEntry', fieldbackground=DARK_ENTRY, foreground=DARK_FG)
        style.configure('TCombobox', fieldbackground=DARK_ENTRY, foreground=DARK_FG)
        style.configure('TNotebook', background=DARK_BG, borderwidth=0)
        style.configure('TNotebook.Tab', background=DARK_BG, foreground=DARK_FG, 
                       padding=[10, 5], font=FONT_BOLD)
        style.map('TNotebook.Tab', 
                 background=[('selected', DARK_SELECTION)],
                 foreground=[('selected', DARK_FG)])
        style.configure('TButton', background=DARK_SELECTION, font=FONT_BOLD)
        style.map('TButton',
                 background=[('active', DARK_TREE)],
                 foreground=[('active', DARK_FG)])
        style.configure('Treeview', background=DARK_TREE, foreground=DARK_FG, 
                       fieldbackground=DARK_TREE, font=FONT)
        style.configure('Treeview.Heading', background=DARK_SELECTION, 
                       foreground=DARK_FG, font=FONT_BOLD)
        style.map('Treeview', 
                 background=[('selected', DARK_SELECTION)],
                 foreground=[('selected', DARK_FG)])

    def _carregar_dados(self):
        self.produtos = DataManager.carregar(DADOS['produtos'])
        self.motoboys = DataManager.carregar(DADOS['motoboys'])
        self.pedidos = DataManager.carregar(DADOS['pedidos'])

    def _criar_interface(self):
        self.abas = ttk.Notebook(self)
        self.abas.pack(fill='both', expand=True, padx=10, pady=10)

        self._criar_aba_produtos()
        self._criar_aba_motoboys()
        self._criar_aba_pedidos()
        self._criar_aba_financeiro()

    def _criar_aba_produtos(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Produtos")

        campos = [
            ("Nome do Produto:", 'entry_nome'),
            ("Quantidade:", 'entry_qtd'),
            ("Preço Unitário (R$):", 'entry_preco')
        ]
        
        for i, (label, var) in enumerate(campos):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            setattr(self, var, ttk.Entry(frame, width=30))
            getattr(self, var).grid(row=i, column=1, pady=5, sticky="ew")

        ttk.Button(frame, text="Adicionar/Atualizar", 
                  command=self._adicionar_produto).grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        self.tree_produtos = ttk.Treeview(frame, columns=("Nome", "Quantidade", "Preço"), show="headings", height=12)
        for col, width in [("Nome", 300), ("Quantidade", 100), ("Preço", 100)]:
            self.tree_produtos.heading(col, text=col)
            self.tree_produtos.column(col, width=width, anchor='center' if col != "Nome" else 'w')
        
        self.tree_produtos.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

        self._atualizar_lista_produtos()

    def _adicionar_produto(self):
        nome = self.entry_nome.get().strip()
        qtd = self.entry_qtd.get().strip()
        preco = self.entry_preco.get().strip()

        if not all([nome, qtd, preco]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        try:
            qtd, preco = int(qtd), float(preco)
            if qtd < 0 or preco < 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Valores inválidos.")
            return

        for p in self.produtos:
            if p['nome'].lower() == nome.lower():
                p.update({'quantidade': qtd, 'preco': preco})
                break
        else:
            self.produtos.append({'nome': nome, 'quantidade': qtd, 'preco': preco})

        DataManager.salvar(DADOS['produtos'], self.produtos)
        self._atualizar_lista_produtos()
        self._limpar_campos([self.entry_nome, self.entry_qtd, self.entry_preco])

    def _atualizar_lista_produtos(self):
        self._limpar_treeview(self.tree_produtos)
        for p in self.produtos:
            self.tree_produtos.insert("", "end", values=(
                p['nome'], 
                p['quantidade'], 
                f"{p['preco']:.2f}"
            ))

    def _criar_aba_motoboys(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Motoboys")

        ttk.Label(frame, text="Nome do Motoboy:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_motoboy_nome = ttk.Entry(frame, width=30)
        self.entry_motoboy_nome.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(frame, text="Valor por entrega (R$):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_motoboy_valor = ttk.Entry(frame, width=30)
        self.entry_motoboy_valor.grid(row=1, column=1, pady=5, sticky="ew")

        ttk.Button(frame, text="Adicionar/Atualizar", 
                  command=self._adicionar_motoboy).grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.tree_motoboys = ttk.Treeview(frame, columns=("Nome", "Valor"), show="headings", height=12)
        for col, width in [("Nome", 300), ("Valor", 150)]:
            self.tree_motoboys.heading(col, text=col)
            self.tree_motoboys.column(col, width=width, anchor='center' if col == "Valor" else 'w')
        
        self.tree_motoboys.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(3, weight=1)

        self._atualizar_lista_motoboys()

    def _adicionar_motoboy(self):
        nome = self.entry_motoboy_nome.get().strip()
        valor = self.entry_motoboy_valor.get().strip()

        if not all([nome, valor]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        try:
            valor = float(valor)
            if valor < 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Valor inválido.")
            return

        for m in self.motoboys:
            if m['nome'].lower() == nome.lower():
                m['valor_por_entrega'] = valor
                break
        else:
            self.motoboys.append({'nome': nome, 'valor_por_entrega': valor})

        DataManager.salvar(DADOS['motoboys'], self.motoboys)
        self._atualizar_lista_motoboys()
        self._limpar_campos([self.entry_motoboy_nome, self.entry_motoboy_valor])

    def _atualizar_lista_motoboys(self):
        self._limpar_treeview(self.tree_motoboys)
        for m in self.motoboys:
            self.tree_motoboys.insert("", "end", values=(
                m['nome'],
                f"{m['valor_por_entrega']:.2f}"
            ))

    def _criar_aba_pedidos(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Pedidos")

        # Data
        ttk.Label(frame, text="Data (DD/MM/AAAA):").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_pedido_data = ttk.Entry(frame, width=20)
        self.entry_pedido_data.grid(row=0, column=1, sticky="ew", pady=5)

        # Produto
        ttk.Label(frame, text="Produto:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_pedidos_produtos = ttk.Combobox(frame, values=[p['nome'] for p in self.produtos], state='readonly')
        self.combo_pedidos_produtos.grid(row=1, column=1, sticky="ew", pady=5)

        # Quantidade
        ttk.Label(frame, text="Quantidade:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_pedido_qtd = ttk.Entry(frame, width=20)
        self.entry_pedido_qtd.grid(row=2, column=1, sticky="ew", pady=5)

        # Motoboy
        ttk.Label(frame, text="Motoboy:").grid(row=3, column=0, sticky="w", pady=5)
        self.combo_pedidos_motoboy = ttk.Combobox(frame, values=[m['nome'] for m in self.motoboys], state='readonly')
        self.combo_pedidos_motoboy.grid(row=3, column=1, sticky="ew", pady=5)

        ttk.Button(frame, text="Adicionar Pedido", command=self._adicionar_pedido).grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        self.tree_pedidos = ttk.Treeview(frame, columns=("Data", "Produto", "Qtd", "Preço Unit", "Motoboy", "Valor Entrega", "Total", "Lucro"), show="headings", height=12)
        cols = [
            ("Data", 100),
            ("Produto", 200),
            ("Qtd", 60),
            ("Preço Unit", 90),
            ("Motoboy", 150),
            ("Valor Entrega", 100),
            ("Total", 100),
            ("Lucro", 100)
        ]
        for col, width in cols:
            self.tree_pedidos.heading(col, text=col)
            self.tree_pedidos.column(col, width=width, anchor='center' if col not in ("Produto", "Motoboy") else 'w')
        self.tree_pedidos.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=10)

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(5, weight=1)

        self._atualizar_lista_pedidos()

    def _adicionar_pedido(self):
        data_str = self.entry_pedido_data.get().strip()
        produto_nome = self.combo_pedidos_produtos.get()
        qtd_str = self.entry_pedido_qtd.get().strip()
        motoboy_nome = self.combo_pedidos_motoboy.get()

        if not all([data_str, produto_nome, qtd_str, motoboy_nome]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        
        # Validar data
        try:
            data = datetime.strptime(data_str, "%d/%m/%Y")
        except:
            messagebox.showerror("Erro", "Data inválida. Use DD/MM/AAAA.")
            return

        try:
            qtd = int(qtd_str)
            if qtd <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        produto = next((p for p in self.produtos if p['nome'] == produto_nome), None)
        if produto is None:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        motoboy = next((m for m in self.motoboys if m['nome'] == motoboy_nome), None)
        if motoboy is None:
            messagebox.showerror("Erro", "Motoboy não encontrado.")
            return

        preco_unit = produto['preco']
        valor_entrega = motoboy['valor_por_entrega']
        total = preco_unit * qtd
        lucro = total * (1 - PERCENTUAL_IFOOD) - valor_entrega

        pedido = {
            'data': data_str,
            'produto': produto_nome,
            'quantidade': qtd,
            'preco_unitario': preco_unit,
            'motoboy': motoboy_nome,
            'valor_entrega': valor_entrega,
            'total': total,
            'lucro': lucro
        }

        self.pedidos.append(pedido)
        DataManager.salvar(DADOS['pedidos'], self.pedidos)

        self._atualizar_lista_pedidos()
        self._limpar_campos([
            self.entry_pedido_data,
            self.combo_pedidos_produtos,
            self.entry_pedido_qtd,
            self.combo_pedidos_motoboy
        ])

        self._atualizar_financeiro()

    def _atualizar_lista_pedidos(self):
        self._limpar_treeview(self.tree_pedidos)
        for p in self.pedidos:
            self.tree_pedidos.insert("", "end", values=(
                p['data'],
                p['produto'],
                p['quantidade'],
                f"{p['preco_unitario']:.2f}",
                p['motoboy'],
                f"{p['valor_entrega']:.2f}",
                f"{p['total']:.2f}",
                f"{p['lucro']:.2f}"
            ))
        self._atualizar_financeiro()

    def _criar_aba_financeiro(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Financeiro")

        self.label_total_vendas = ttk.Label(frame, text="Total Vendas (R$): 0.00", font=FONT_BOLD)
        self.label_total_vendas.grid(row=0, column=0, sticky="w", pady=5)

        self.label_total_motoboys = ttk.Label(frame, text="Total Pago aos Motoboys (R$): 0.00", font=FONT_BOLD)
        self.label_total_motoboys.grid(row=1, column=0, sticky="w", pady=5)

        self.label_total_lucro = ttk.Label(frame, text="Lucro Líquido (R$): 0.00", font=FONT_BOLD)
        self.label_total_lucro.grid(row=2, column=0, sticky="w", pady=5)

        self._atualizar_financeiro()

    def _atualizar_financeiro(self):
        total_vendas = sum(p['total'] for p in self.pedidos)
        total_motoboys = sum(p['valor_entrega'] for p in self.pedidos)
        lucro = sum(p['lucro'] for p in self.pedidos)

        if hasattr(self, 'label_total_vendas'):
            self.label_total_vendas.config(text=f"Total Vendas (R$): {total_vendas:.2f}")
            self.label_total_motoboys.config(text=f"Total Pago aos Motoboys (R$): {total_motoboys:.2f}")
            self.label_total_lucro.config(text=f"Lucro Líquido (R$): {lucro:.2f}")

    def _limpar_treeview(self, tree):
        for i in tree.get_children():
            tree.delete(i)

    def _limpar_campos(self, widgets):
        for w in widgets:
            if isinstance(w, ttk.Combobox):
                w.set('')
            else:
                w.delete(0, 'end')

    def _atualizar_combos(self):
        # Atualiza os combos na aba pedidos com os dados atuais
        produtos_nomes = [p['nome'] for p in self.produtos]
        motoboys_nomes = [m['nome'] for m in self.motoboys]
        self.combo_pedidos_produtos.config(values=produtos_nomes)
        self.combo_pedidos_motoboy.config(values=motoboys_nomes)

    def run(self):
        self._atualizar_combos()
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
