import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

# Configurações
DARK_BG = '#1a1a1a'
ACCENT_COLOR = '#ff4500'
HIGHLIGHT_COLOR = '#ffa500'
FONT = ('Arial', 10)
FONT_BOLD = ('Arial', 10, 'bold')

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
        
        # Configurações gerais
        style.configure('.', background=DARK_BG, foreground='white', font=FONT)
        style.configure('TNotebook', borderwidth=0)
        style.configure('TNotebook.Tab', background='#333', padding=[10, 5], font=FONT_BOLD)
        style.map('TNotebook.Tab', 
                 background=[('selected', HIGHLIGHT_COLOR)],
                 foreground=[('selected', 'black')])
        
        # Botões
        style.configure('TButton', background=ACCENT_COLOR, font=FONT_BOLD)
        style.map('TButton',
                 background=[('active', HIGHLIGHT_COLOR)],
                 foreground=[('active', 'black')])
        
        # Treeview
        style.configure('Treeview', background='#2a2a2a', fieldbackground='#2a2a2a')
        style.configure('Treeview.Heading', background=ACCENT_COLOR, font=FONT_BOLD)
        style.map('Treeview', 
                 background=[('selected', HIGHLIGHT_COLOR)],
                 foreground=[('selected', 'black')])

    def _carregar_dados(self):
        self.produtos = DataManager.carregar(DADOS['produtos'])
        self.motoboys = DataManager.carregar(DADOS['motoboys'])
        self.pedidos = DataManager.carregar(DADOS['pedidos'])

    def _criar_interface(self):
        # Notebook principal
        self.abas = ttk.Notebook(self)
        self.abas.pack(fill='both', expand=True, padx=10, pady=10)

        # Abas
        self._criar_aba_produtos()
        self._criar_aba_motoboys()
        self._criar_aba_pedidos()
        self._criar_aba_financeiro()

    def _criar_aba_produtos(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Produtos")

        # Formulário
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

        # Lista de produtos
        self.tree_produtos = ttk.Treeview(frame, columns=("Nome", "Quantidade", "Preço"), show="headings", height=12)
        for col, width in [("Nome", 300), ("Quantidade", 100), ("Preço", 100)]:
            self.tree_produtos.heading(col, text=col)
            self.tree_produtos.column(col, width=width, anchor='center' if col != "Nome" else 'w')
        
        self.tree_produtos.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")
        self._atualizar_lista_produtos()

        # Configuração de grid
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

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

        # Atualiza ou adiciona produto
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

        # Formulário
        ttk.Label(frame, text="Nome do Motoboy:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_motoboy_nome = ttk.Entry(frame, width=30)
        self.entry_motoboy_nome.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(frame, text="Valor por entrega (R$):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_motoboy_valor = ttk.Entry(frame, width=30)
        self.entry_motoboy_valor.grid(row=1, column=1, pady=5, sticky="ew")

        ttk.Button(frame, text="Adicionar/Atualizar", 
                  command=self._adicionar_motoboy).grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        # Lista de motoboys
        self.tree_motoboys = ttk.Treeview(frame, columns=("Nome", "Valor"), show="headings", height=12)
        for col, width in [("Nome", 300), ("Valor", 150)]:
            self.tree_motoboys.heading(col, text=col)
            self.tree_motoboys.column(col, width=width, anchor='center' if col == "Valor" else 'w')
        
        self.tree_motoboys.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")
        self._atualizar_lista_motoboys()

        # Configuração de grid
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(3, weight=1)

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

        # Atualiza ou adiciona motoboy
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

        # Formulário
        campos = [
            ("Tipo do Pedido:", 'combo_tipo', ['Loja', 'iFood', 'Robô']),
            ("Produto:", 'combo_produto', []),
            ("Quantidade:", 'entry_pedido_qtd', None),
            ("Motoboy:", 'combo_motoboy', [])
        ]

        for i, (label, var, values) in enumerate(campos):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            
            if values is not None:
                widget = ttk.Combobox(frame, values=values, state="readonly", width=27)
                if values: widget.current(0)
            else:
                widget = ttk.Entry(frame, width=30)
            
            setattr(self, var, widget)
            widget.grid(row=i, column=1, pady=5, sticky="ew")

        ttk.Button(frame, text="Adicionar Pedido", 
                  command=self._adicionar_pedido).grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        # Lista de pedidos
        cols = [("Data", 140), ("Tipo", 80), ("Produto", 200), 
                ("Qtd", 60), ("Valor", 100), ("Motoboy", 150), ("Total", 100)]
        
        self.tree_pedidos = ttk.Treeview(frame, columns=[c[0] for c in cols], show="headings", height=12)
        for col, width in cols:
            self.tree_pedidos.heading(col, text=col)
            self.tree_pedidos.column(col, width=width, anchor='center' if col not in ["Produto", "Motoboy"] else 'w')
        
        self.tree_pedidos.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")
        self._atualizar_lista_pedidos()

        # Atualizar comboboxes
        self._atualizar_comboboxes()

        # Configuração de grid
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(5, weight=1)

    def _adicionar_pedido(self):
        dados = {
            'tipo': self.combo_tipo.get(),
            'produto': self.combo_produto.get(),
            'quantidade': self.entry_pedido_qtd.get().strip(),
            'motoboy': self.combo_motoboy.get()
        }

        if not all(dados.values()):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        try:
            qtd = int(dados['quantidade'])
            if qtd <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        # Busca produto e motoboy
        produto = next((p for p in self.produtos if p['nome'] == dados['produto']), None)
        motoboy = next((m for m in self.motoboys if m['nome'] == dados['motoboy']), None)

        if not produto or not motoboy:
            messagebox.showerror("Erro", "Produto ou motoboy não encontrado.")
            return

        # Calcula preço (com taxa para iFood)
        preco = produto['preco']
        if dados['tipo'] == 'iFood':
            preco = round(preco * (1 + PERCENTUAL_IFOOD), 2)

        # Cria pedido
        pedido = {
            'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'tipo': dados['tipo'],
            'produto': dados['produto'],
            'quantidade': qtd,
            'preco_unitario': preco,
            'motoboy': dados['motoboy'],
            'total': preco * qtd
        }

        self.pedidos.append(pedido)
        DataManager.salvar(DADOS['pedidos'], self.pedidos)
        self._atualizar_lista_pedidos()
        self.entry_pedido_qtd.delete(0, tk.END)

    def _atualizar_lista_pedidos(self):
        self._limpar_treeview(self.tree_pedidos)
        for p in self.pedidos:
            self.tree_pedidos.insert("", "end", values=(
                p['data'],
                p['tipo'],
                p['produto'],
                p['quantidade'],
                f"{p['preco_unitario']:.2f}",
                p['motoboy'],
                f"{p['total']:.2f}"
            ))

    def _criar_aba_financeiro(self):
        frame = ttk.Frame(self.abas, padding=20)
        self.abas.add(frame, text="Financeiro")

        # Painel de resultados
        self.lbl_vendas = ttk.Label(frame, text="Total Vendas: R$ 0.00", font=('Arial', 14))
        self.lbl_vendas.pack(pady=15)

        self.lbl_motoboys = ttk.Label(frame, text="Total Motoboys: R$ 0.00", font=('Arial', 14))
        self.lbl_motoboys.pack(pady=15)

        self.lbl_lucro = ttk.Label(frame, text="Lucro Líquido: R$ 0.00", font=('Arial', 16, 'bold'))
        self.lbl_lucro.pack(pady=20)

        ttk.Button(frame, text="Calcular", command=self._calcular_financeiro).pack(pady=10)

    def _calcular_financeiro(self):
        total_vendas = sum(p['total'] for p in self.pedidos)
        total_motoboys = sum(
            next((m['valor_por_entrega'] for m in self.motoboys if m['nome'] == p['motoboy']), 0)
            for p in self.pedidos
        )
        lucro = total_vendas - total_motoboys

        self.lbl_vendas.config(text=f"Total Vendas: R$ {total_vendas:.2f}")
        self.lbl_motoboys.config(text=f"Total Motoboys: R$ {total_motoboys:.2f}")
        self.lbl_lucro.config(text=f"Lucro Líquido: R$ {lucro:.2f}")

    def _atualizar_comboboxes(self):
        self.combo_produto['values'] = [p['nome'] for p in self.produtos]
        self.combo_motoboy['values'] = [m['nome'] for m in self.motoboys]
        if self.produtos: self.combo_produto.current(0)
        if self.motoboys: self.combo_motoboy.current(0)

    def _limpar_treeview(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def _limpar_campos(self, widgets):
        for widget in widgets:
            widget.delete(0, tk.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()