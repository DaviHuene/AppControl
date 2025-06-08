import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

# Configurações de Cores
DARK_BG = '#121212'
DARK_FG = "#03F7AE"
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
        self.title("Garagem do Frango - Control")
        self.geometry("1000x700")
        self.configure(bg=DARK_BG)

        self._configurar_estilo()
        self._carregar_dados()
        self._criar_menu_contexto()
        self._criar_interface()

    def _configurar_estilo(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('.', background=DARK_BG, foreground=DARK_FG, font=FONT)
        style.configure('TFrame', background=DARK_BG)
        style.configure('TLabel', background=DARK_BG, foreground=DARK_FG)
        style.configure('TEntry', fieldbackground=DARK_ENTRY, foreground=DARK_FG)
        style.configure('TCombobox', fieldbackground=DARK_ENTRY, foreground=DARK_FG)
        style.configure('Dark.TEntry', fieldbackground='#2d2d2d', foreground=DARK_FG, insertcolor=DARK_FG)
        style.configure('Dark.TCombobox', fieldbackground='#2d2d2d', foreground=DARK_FG)
        style.map('Dark.TCombobox', fieldbackground=[('readonly', '#2d2d2d')], selectbackground=[('readonly', '#3d3d3d')])
        style.configure('Treeview', background=DARK_TREE, foreground=DARK_FG, fieldbackground=DARK_TREE, font=FONT)
        style.configure('Treeview.Heading', background=DARK_SELECTION, foreground=DARK_FG, font=FONT_BOLD)
        style.map('Treeview', background=[('selected', DARK_SELECTION)], foreground=[('selected', DARK_FG)])

    def _carregar_dados(self):
        self.produtos = DataManager.carregar(DADOS['produtos'])
        self.motoboys = DataManager.carregar(DADOS['motoboys'])
        self.pedidos = DataManager.carregar(DADOS['pedidos'])

    def _criar_menu_contexto(self):
        pass  # Pode adicionar menu contextual se desejar

    def _criar_interface(self):
        self.abas = ttk.Notebook(self)
        self.abas.pack(fill='both', expand=True, padx=10, pady=10)
        self._criar_aba_pedidos()

    def _criar_aba_pedidos(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Pedidos")

        self.lista_produtos_temp = []

        ttk.Label(frame, text="Nome do Cliente:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_cliente = ttk.Entry(frame, width=30, style='Dark.TEntry')
        self.entry_cliente.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(frame, text="Tipo do Pedido:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_tipo = ttk.Combobox(frame, values=['Loja', 'iFood', 'Robô'], 
                                       state="readonly", width=27, style='Dark.TCombobox')
        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=1, column=1, pady=5, sticky="ew")

        ttk.Label(frame, text="Produto:").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_produto = ttk.Combobox(frame, state="readonly", width=27, style='Dark.TCombobox')
        self.combo_produto.grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Label(frame, text="Quantidade:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_pedido_qtd = ttk.Entry(frame, width=30, style='Dark.TEntry')
        self.entry_pedido_qtd.grid(row=3, column=1, pady=5, sticky="ew")

        ttk.Button(frame, text="Adicionar Produto ao Pedido", command=self._adicionar_produto_temp)
        .grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

        self.label_produtos_selecionados = ttk.Label(frame, text="Produtos no Pedido: 0", foreground="#aaa")
        self.label_produtos_selecionados.grid(row=5, column=0, columnspan=2, pady=5)

        self.motoboy_frame = ttk.Frame(frame)
        self.motoboy_frame.grid(row=6, column=0, columnspan=2, sticky="ew")
        ttk.Label(self.motoboy_frame, text="Motoboy:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_motoboy = ttk.Combobox(self.motoboy_frame, state="readonly", width=27, style='Dark.TCombobox')
        self.combo_motoboy.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Button(frame, text="Finalizar Pedido", command=self._adicionar_pedido)
        .grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

        cols = ["ID", "Cliente", "Data", "Tipo", "Produtos", "Motoboy", "Total"]
        self.tree_pedidos = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        for col in cols:
            self.tree_pedidos.heading(col, text=col)
            self.tree_pedidos.column(col, width=120, anchor='w')
        self.tree_pedidos.grid(row=8, column=0, columnspan=2, pady=10, sticky="nsew")

        self._atualizar_comboboxes()
        self._atualizar_lista_pedidos()

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(8, weight=1)

    def _adicionar_produto_temp(self):
        produto = self.combo_produto.get()
        qtd_str = self.entry_pedido_qtd.get().strip()

        if not produto or not qtd_str:
            messagebox.showerror("Erro", "Selecione o produto e a quantidade.")
            return

        try:
            qtd = int(qtd_str)
            if qtd <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        produto_obj = next((p for p in self.produtos if p['nome'] == produto), None)
        if not produto_obj:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        if produto_obj['quantidade'] < qtd:
            messagebox.showerror("Erro", f"Estoque insuficiente. Disponível: {produto_obj['quantidade']}")
            return

        self.lista_produtos_temp.append({
            'nome': produto,
            'quantidade': qtd,
            'preco': produto_obj['preco']
        })

        self.label_produtos_selecionados.config(text=f"Produtos no Pedido: {len(self.lista_produtos_temp)}")
        self.entry_pedido_qtd.delete(0, tk.END)

    def _adicionar_pedido(self):
        cliente = self.entry_cliente.get().strip()
        tipo = self.combo_tipo.get()
        motoboy = self.combo_motoboy.get() if tipo in ['iFood', 'Robô'] else "Retirada na Loja"

        if not cliente or not self.lista_produtos_temp:
            messagebox.showerror("Erro", "Informe o cliente e adicione ao menos um produto.")
            return

        if tipo in ['iFood', 'Robô'] and not motoboy:
            messagebox.showerror("Erro", "Selecione um motoboy.")
            return

        total = 0
        for item in self.lista_produtos_temp:
            produto_obj = next((p for p in self.produtos if p['nome'] == item['nome']), None)
            if produto_obj:
                produto_obj['quantidade'] -= item['quantidade']
                preco = item['preco']
                if tipo == 'iFood':
                    preco *= (1 + PERCENTUAL_IFOOD)
                item['preco'] = round(preco, 2)
                item['subtotal'] = round(preco * item['quantidade'], 2)
                total += item['subtotal']

        pedido_id = max([p.get('id', 0) for p in self.pedidos] + [0]) + 1
        pedido = {
            'id': pedido_id,
            'cliente': cliente,
            'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'tipo': tipo,
            'produtos': self.lista_produtos_temp,
            'motoboy': motoboy,
            'total': round(total, 2)
        }

        self.pedidos.append(pedido)
        DataManager.salvar(DADOS['pedidos'], self.pedidos)
        DataManager.salvar(DADOS['produtos'], self.produtos)

        self.lista_produtos_temp = []
        self.label_produtos_selecionados.config(text="Produtos no Pedido: 0")
        self._atualizar_lista_pedidos()
        self._atualizar_lista_produtos()
        self._limpar_campos([self.entry_cliente])

    def _atualizar_lista_pedidos(self):
        self._limpar_treeview(self.tree_pedidos)
        for p in sorted(self.pedidos, key=lambda x: x.get('id', 0), reverse=True):
            nomes = ', '.join([f"{prod['nome']} (x{prod['quantidade']})" for prod in p.get('produtos', [])])
            self.tree_pedidos.insert("", "end", values=(
                p.get('id', ''),
                p.get('cliente', ''),
                p['data'],
                p['tipo'],
                nomes,
                p['motoboy'],
                f"{p['total']:.2f}"
            ))

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