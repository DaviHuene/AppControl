import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

# Arquivos de dados
DADOS = {
    'produtos': 'produtos.json',
    'motoboys': 'motoboys.json',
    'pedidos': 'pedidos.json'
}

# Taxa do iFood (exemplo: 20%)
PERCENTUAL_IFOOD = 0.20

def carregar_dados(arquivo):
    if not os.path.exists(arquivo):
        return []
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Garagem do Frango - Controle de Vendas")
        self.geometry("1000x700")
        self.configure(bg='#1a1a1a')
        
        # Estilo ttk customizado
        style = ttk.Style(self)
        style.theme_use('clam')  # tema básico para customizar
        style.configure('TNotebook', background='#1a1a1a', borderwidth=0)
        style.configure('TNotebook.Tab', background='#333333', foreground='white', padding=[10, 8], font=('Arial', 11, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#ffa500')], foreground=[('selected', 'black')])  # amarelo quando ativo
        style.configure('TLabel', background='#1a1a1a', foreground='white', font=('Arial', 11))
        style.configure('TButton', background='#ff4500', foreground='white', font=('Arial', 11, 'bold'), padding=6)
        style.map('TButton',
                  background=[('active', '#ffa500'), ('!disabled', '#ff4500')],
                  foreground=[('active', 'black')])
        style.configure('Treeview', background='#2a2a2a', foreground='white', fieldbackground='#2a2a2a', font=('Arial', 10))
        style.configure('Treeview.Heading', background='#ff4500', foreground='white', font=('Arial', 11, 'bold'))
        style.map('Treeview', background=[('selected', '#ffa500')], foreground=[('selected', 'black')])
        
        # Dados carregados
        self.produtos = carregar_dados(DADOS['produtos'])
        self.motoboys = carregar_dados(DADOS['motoboys'])
        self.pedidos = carregar_dados(DADOS['pedidos'])

        # Notebook (abas)
        self.aba_control = ttk.Notebook(self)
        self.aba_control.pack(fill='both', expand=True, padx=10, pady=10)

        # Criar abas
        self.frame_produtos()
        self.frame_motoboys()
        self.frame_pedidos()
        self.frame_finalizar()

        # Atualiza combobox e listas
        self.atualizar_combobox_produtos()
        self.atualizar_combobox_motoboys()
        self.atualizar_lista_produtos()
        self.atualizar_lista_motoboys()
        self.atualizar_lista_pedidos()

    # --- ABA PRODUTOS ---
    def frame_produtos(self):
        frame = ttk.Frame(self.aba_control, padding=15)
        self.aba_control.add(frame, text="Produtos")

        ttk.Label(frame, text="Nome do Produto:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome_produto = ttk.Entry(frame, width=35)
        self.entry_nome_produto.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Quantidade:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_qtd_produto = ttk.Entry(frame, width=35)
        self.entry_qtd_produto.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Preço Unitário (R$):").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_preco_produto = ttk.Entry(frame, width=35)
        self.entry_preco_produto.grid(row=2, column=1, pady=5)

        btn_add_produto = ttk.Button(frame, text="Adicionar/Atualizar Produto", command=self.adicionar_produto)
        btn_add_produto.grid(row=3, column=0, columnspan=2, pady=15, sticky="ew")

        # Treeview produtos
        self.tree_produtos = ttk.Treeview(frame, columns=("Nome", "Quantidade", "Preço"), show="headings", height=10)
        self.tree_produtos.heading("Nome", text="Nome")
        self.tree_produtos.heading("Quantidade", text="Quantidade")
        self.tree_produtos.heading("Preço", text="Preço (R$)")
        self.tree_produtos.column("Nome", width=300)
        self.tree_produtos.column("Quantidade", width=120, anchor='center')
        self.tree_produtos.column("Preço", width=120, anchor='center')
        self.tree_produtos.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

        frame.rowconfigure(4, weight=1)
        frame.columnconfigure(1, weight=1)

    def adicionar_produto(self):
        nome = self.entry_nome_produto.get().strip()
        qtd = self.entry_qtd_produto.get().strip()
        preco = self.entry_preco_produto.get().strip()
        if not nome or not qtd or not preco:
            messagebox.showerror("Erro", "Preencha todos os campos do produto.")
            return
        try:
            qtd = int(qtd)
            preco = float(preco)
            if qtd < 0 or preco < 0:
                messagebox.showerror("Erro", "Quantidade e preço devem ser positivos.")
                return
        except:
            messagebox.showerror("Erro", "Quantidade deve ser inteiro e preço deve ser número.")
            return

        # Atualizar produto existente ou adicionar novo
        for p in self.produtos:
            if p['nome'].lower() == nome.lower():
                p['quantidade'] = qtd
                p['preco'] = preco
                break
        else:
            self.produtos.append({'nome': nome, 'quantidade': qtd, 'preco': preco})

        salvar_dados(DADOS['produtos'], self.produtos)
        self.atualizar_lista_produtos()
        self.atualizar_combobox_produtos()  # atualizar pedidos

        self.entry_nome_produto.delete(0, tk.END)
        self.entry_qtd_produto.delete(0, tk.END)
        self.entry_preco_produto.delete(0, tk.END)

    def atualizar_lista_produtos(self):
        for i in self.tree_produtos.get_children():
            self.tree_produtos.delete(i)
        for p in self.produtos:
            self.tree_produtos.insert("", "end", values=(p['nome'], p['quantidade'], f"{p['preco']:.2f}"))

    def atualizar_combobox_produtos(self):
        nomes = [p['nome'] for p in self.produtos]
        if hasattr(self, 'combo_produtos'):
            self.combo_produtos['values'] = nomes
            if nomes:
                self.combo_produtos.current(0)

    # --- ABA MOTOboys ---
    def frame_motoboys(self):
        frame = ttk.Frame(self.aba_control, padding=15)
        self.aba_control.add(frame, text="Motoboys")

        ttk.Label(frame, text="Nome do Motoboy:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome_motoboy = ttk.Entry(frame, width=35)
        self.entry_nome_motoboy.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Valor por entrega (R$):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_valor_motoboy = ttk.Entry(frame, width=35)
        self.entry_valor_motoboy.grid(row=1, column=1, pady=5)

        btn_add_motoboy = ttk.Button(frame, text="Adicionar/Atualizar Motoboy", command=self.adicionar_motoboy)
        btn_add_motoboy.grid(row=2, column=0, columnspan=2, pady=15, sticky="ew")

        self.tree_motoboys = ttk.Treeview(frame, columns=("Nome", "Valor"), show="headings", height=10)
        self.tree_motoboys.heading("Nome", text="Nome")
        self.tree_motoboys.heading("Valor", text="Valor por entrega (R$)")
        self.tree_motoboys.column("Nome", width=300)
        self.tree_motoboys.column("Valor", width=150, anchor='center')
        self.tree_motoboys.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

        frame.rowconfigure(3, weight=1)
        frame.columnconfigure(1, weight=1)

    def adicionar_motoboy(self):
        nome = self.entry_nome_motoboy.get().strip()
        valor = self.entry_valor_motoboy.get().strip()
        if not nome or not valor:
            messagebox.showerror("Erro", "Preencha todos os campos do motoboy.")
            return
        try:
            valor = float(valor)
            if valor < 0:
                messagebox.showerror("Erro", "Valor deve ser positivo.")
                return
        except:
            messagebox.showerror("Erro", "Valor deve ser número.")
            return

        # Atualizar ou adicionar
        for m in self.motoboys:
            if m['nome'].lower() == nome.lower():
                m['valor_por_entrega'] = valor
                break
        else:
            self.motoboys.append({'nome': nome, 'valor_por_entrega': valor})

        salvar_dados(DADOS['motoboys'], self.motoboys)
        self.atualizar_lista_motoboys()
        self.atualizar_combobox_motoboys()

        self.entry_nome_motoboy.delete(0, tk.END)
        self.entry_valor_motoboy.delete(0, tk.END)

    def atualizar_lista_motoboys(self):
        for i in self.tree_motoboys.get_children():
            self.tree_motoboys.delete(i)
        for m in self.motoboys:
            self.tree_motoboys.insert("", "end", values=(m['nome'], f"{m['valor_por_entrega']:.2f}"))

    def atualizar_combobox_motoboys(self):
        nomes = [m['nome'] for m in self.motoboys]
        if hasattr(self, 'combo_motoboys'):
            self.combo_motoboys['values'] = nomes
            if nomes:
                self.combo_motoboys.current(0)

    # --- ABA PEDIDOS ---
    def frame_pedidos(self):
        frame = ttk.Frame(self.aba_control, padding=15)
        self.aba_control.add(frame, text="Pedidos")

        # Tipo de pedido
        ttk.Label(frame, text="Tipo do Pedido:").grid(row=0, column=0, sticky='w', pady=5)
        self.combo_tipo_pedido = ttk.Combobox(frame, values=['Loja', 'iFood', 'Robô'], state="readonly")
        self.combo_tipo_pedido.grid(row=0, column=1, sticky='ew', pady=5)
        self.combo_tipo_pedido.current(0)

        # Produto
        ttk.Label(frame, text="Produto:").grid(row=1, column=0, sticky='w', pady=5)
        self.combo_produtos = ttk.Combobox(frame, state="readonly")
        self.combo_produtos.grid(row=1, column=1, sticky='ew', pady=5)

        # Quantidade do pedido
        ttk.Label(frame, text="Quantidade:").grid(row=2, column=0, sticky='w', pady=5)
        self.entry_qtd_pedido = ttk.Entry(frame)
        self.entry_qtd_pedido.grid(row=2, column=1, sticky='ew', pady=5)

        # Motoboy
        ttk.Label(frame, text="Motoboy:").grid(row=3, column=0, sticky='w', pady=5)
        self.combo_motoboys = ttk.Combobox(frame, state="readonly")
        self.combo_motoboys.grid(row=3, column=1, sticky='ew', pady=5)

        btn_add_pedido = ttk.Button(frame, text="Adicionar Pedido", command=self.adicionar_pedido)
        btn_add_pedido.grid(row=4, column=0, columnspan=2, pady=15, sticky="ew")

        # Treeview pedidos
        self.tree_pedidos = ttk.Treeview(frame, columns=("Data", "Tipo", "Produto", "Qtd", "Valor Unit.", "Motoboy", "Total"), show="headings", height=10)
        self.tree_pedidos.heading("Data", text="Data/Hora")
        self.tree_pedidos.heading("Tipo", text="Tipo")
        self.tree_pedidos.heading("Produto", text="Produto")
        self.tree_pedidos.heading("Qtd", text="Qtd")
        self.tree_pedidos.heading("Valor Unit.", text="Valor Unit. (R$)")
        self.tree_pedidos.heading("Motoboy", text="Motoboy")
        self.tree_pedidos.heading("Total", text="Total (R$)")
        self.tree_pedidos.column("Data", width=140)
        self.tree_pedidos.column("Tipo", width=80, anchor='center')
        self.tree_pedidos.column("Produto", width=250)
        self.tree_pedidos.column("Qtd", width=50, anchor='center')
        self.tree_pedidos.column("Valor Unit.", width=100, anchor='center')
        self.tree_pedidos.column("Motoboy", width=150)
        self.tree_pedidos.column("Total", width=100, anchor='center')
        self.tree_pedidos.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")

        frame.rowconfigure(5, weight=1)
        frame.columnconfigure(1, weight=1)

    def adicionar_pedido(self):
        tipo = self.combo_tipo_pedido.get()
        produto_nome = self.combo_produtos.get()
        qtd_str = self.entry_qtd_pedido.get()
        motoboy_nome = self.combo_motoboys.get()

        if not produto_nome or not qtd_str or not motoboy_nome:
            messagebox.showerror("Erro", "Preencha todos os campos do pedido.")
            return
        try:
            qtd = int(qtd_str)
            if qtd <= 0:
                messagebox.showerror("Erro", "Quantidade deve ser maior que zero.")
                return
        except:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        # Buscar produto para pegar preço base
        produto = None
        for p in self.produtos:
            if p['nome'] == produto_nome:
                produto = p
                break
        if produto is None:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        # Ajustar preço para iFood (exemplo taxa de 20% sobre o preço base)
        preco_unitario = produto['preco']
        if tipo == 'iFood':
            preco_unitario = round(preco_unitario * (1 + PERCENTUAL_IFOOD), 2)

        # Buscar motoboy para pegar valor por entrega
        motoboy = None
        for m in self.motoboys:
            if m['nome'] == motoboy_nome:
                motoboy = m
                break
        if motoboy is None:
            messagebox.showerror("Erro", "Motoboy não encontrado.")
            return

        # Calcular total
        total = preco_unitario * qtd

        # Salvar pedido
        pedido = {
            'data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'tipo': tipo,
            'produto': produto_nome,
            'quantidade': qtd,
            'preco_unitario': preco_unitario,
            'motoboy': motoboy_nome,
            'total': total
        }
        self.pedidos.append(pedido)
        salvar_dados(DADOS['pedidos'], self.pedidos)

        self.atualizar_lista_pedidos()

        # Limpar entradas
        self.entry_qtd_pedido.delete(0, tk.END)

    def atualizar_lista_pedidos(self):
        for i in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(i)
        for p in self.pedidos:
            cliente = p.get('cliente', '---')
            data = p.get('data', '---')
            tipo = p.get('tipo', '---')
            produto = p.get('produto', '---')
            quantidade = p.get('quantidade', 0)
            preco_unitario = p.get('preco_unitario', 0.0)
            motoboy = p.get('motoboy', '---')
            total = p.get('total', 0.0)

            self.tree_pedidos.insert("", "end", values=(
                cliente, data, tipo, produto, quantidade,
                f"{preco_unitario:.2f}", motoboy, f"{total:.2f}"
            ))

    # --- ABA FINALIZAR E GANHOS ---
    def frame_finalizar(self):
        frame = ttk.Frame(self.aba_control, padding=15)
        self.aba_control.add(frame, text="Ganhos e Pagamentos")

        self.label_total_vendas = ttk.Label(frame, text="Total vendas: R$ 0.00", font=('Arial', 14, 'bold'), foreground='#ffa500')
        self.label_total_vendas.pack(pady=15)

        self.label_total_pagar_motoboys = ttk.Label(frame, text="Total a pagar motoboys: R$ 0.00", font=('Arial', 14, 'bold'), foreground='#ff4500')
        self.label_total_pagar_motoboys.pack(pady=15)

        btn_calcular = ttk.Button(frame, text="Calcular Totais", command=self.calcular_totais)
        btn_calcular.pack(pady=10)

    def calcular_totais(self):
        total_vendas = sum(p['total'] for p in self.pedidos)
        total_pagar_motoboys = 0
        for p in self.pedidos:
            motoboy = next((m for m in self.motoboys if m['nome'] == p['motoboy']), None)
            if motoboy:
                total_pagar_motoboys += motoboy['valor_por_entrega']

        self.label_total_vendas.config(text=f"Total vendas: R$ {total_vendas:.2f}")
        self.label_total_pagar_motoboys.config(text=f"Total a pagar motoboys: R$ {total_pagar_motoboys:.2f}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
