import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
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
        self.geometry("1200x800")
        self.configure(bg=DARK_BG)
        
        self._configurar_estilo()
        self._carregar_dados()
        self._criar_menu_contexto()
        self._criar_interface()
        
        # Lista temporária para produtos do pedido
        self.produtos_pedido = []

    def _configurar_estilo(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        
        # Configurações gerais
        style.configure('.', background=DARK_BG, foreground=DARK_FG, font=FONT)
        style.configure('TFrame', background=DARK_BG)
        style.configure('TLabel', background=DARK_BG, foreground=DARK_FG)
        style.configure('TEntry', fieldbackground=DARK_ENTRY, foreground=DARK_FG)
        style.configure('TCombobox', fieldbackground=DARK_ENTRY, foreground=DARK_FG)
        
        # Notebook
        style.configure('TNotebook', background=DARK_BG, borderwidth=0)
        style.configure('TNotebook.Tab', background=DARK_BG, foreground=DARK_FG, 
                       padding=[10, 5], font=FONT_BOLD)
        style.map('TNotebook.Tab', 
                 background=[('selected', DARK_SELECTION)],
                 foreground=[('selected', DARK_FG)])
        
        # Botões
        style.configure('TButton', background=DARK_SELECTION, font=FONT_BOLD)
        style.map('TButton',
                 background=[('active', DARK_TREE)],
                 foreground=[('active', DARK_FG)])
        
        # Treeview
        style.configure('Treeview', background=DARK_TREE, foreground=DARK_FG, 
                       fieldbackground=DARK_TREE, font=FONT)
        style.configure('Treeview.Heading', background=DARK_SELECTION, 
                       foreground=DARK_FG, font=FONT_BOLD)
        style.map('Treeview', 
                 background=[('selected', DARK_SELECTION)],
                 foreground=[('selected', DARK_FG)])

    def _criar_menu_contexto(self):
        self.menu_contexto = tk.Menu(self, tearoff=0)
        self.menu_contexto.add_command(label="Editar", command=self._editar_item_selecionado)
        self.menu_contexto.add_command(label="Excluir", command=self._excluir_item_selecionado)
        self.menu_contexto.add_separator()
        self.menu_contexto.add_command(label="Excluir Selecionados (Massa)", command=self._excluir_selecionados_massa)
        
        self.bind("<Button-3>", self._mostrar_menu_contexto)

    def _mostrar_menu_contexto(self, event):
        widget = event.widget
        if isinstance(widget, ttk.Treeview):
            item = widget.identify_row(event.y)
            if item:
                if item not in widget.selection():
                    widget.selection_set(item)
                self.menu_contexto.post(event.x_root, event.y_root)

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

    # ... (métodos de produtos e motoboys permanecem os mesmos) ...

    def _criar_aba_pedidos(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Pedidos")

        # Frame esquerdo - Formulário
        left_frame = ttk.Frame(frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Frame direito - Descrição do Pedido
        right_frame = ttk.Frame(frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Configurar pesos
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

        # Formulário de Pedido
        ttk.Label(left_frame, text="Nome do Cliente:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_cliente = ttk.Entry(left_frame, width=30)
        self.entry_cliente.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(left_frame, text="Tipo do Pedido:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_tipo = ttk.Combobox(left_frame, values=['Loja', 'iFood', 'Robô'], state="readonly", width=27)
        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=1, column=1, pady=5, sticky="ew")
        self.combo_tipo.bind('<<ComboboxSelected>>', self._atualizar_visibilidade_motoboy)

        # Frame para adicionar produtos
        produto_frame = ttk.Frame(left_frame)
        produto_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        ttk.Label(produto_frame, text="Produto:").grid(row=0, column=0, sticky="w")
        self.combo_produto = ttk.Combobox(produto_frame, state="readonly", width=20)
        self.combo_produto.grid(row=0, column=1, sticky="ew")

        ttk.Label(produto_frame, text="Quantidade:").grid(row=0, column=2, sticky="w", padx=5)
        self.entry_pedido_qtd = ttk.Entry(produto_frame, width=8)
        self.entry_pedido_qtd.grid(row=0, column=3, sticky="ew")

        ttk.Button(produto_frame, text="+", width=3, 
                  command=self._adicionar_produto_pedido).grid(row=0, column=4, padx=5)

        # Frame para motoboy
        self.motoboy_frame = ttk.Frame(left_frame)
        self.motoboy_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        
        ttk.Label(self.motoboy_frame, text="Motoboy:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_motoboy = ttk.Combobox(self.motoboy_frame, state="readonly", width=27)
        self.combo_motoboy.grid(row=0, column=1, pady=5, sticky="ew")

        # Treeview para produtos do pedido
        self.tree_produtos_pedido = ttk.Treeview(left_frame, columns=("Produto", "Qtd", "Preço", "Total"), 
                                               show="headings", height=5)
        for col, width in [("Produto", 200), ("Qtd", 60), ("Preço", 80), ("Total", 80)]:
            self.tree_produtos_pedido.heading(col, text=col)
            self.tree_produtos_pedido.column(col, width=width, anchor='center' if col != "Produto" else 'w')
        self.tree_produtos_pedido.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

        # Botões
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Button(btn_frame, text="Adicionar Pedido", command=self._adicionar_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self._limpar_pedido).pack(side=tk.LEFT, padx=5)

        # Área de descrição do pedido
        ttk.Label(right_frame, text="Descrição do Pedido", font=FONT_BOLD).pack(pady=5)
        
        self.descricao_pedido = scrolledtext.ScrolledText(right_frame, width=50, height=15, 
                                                        bg=DARK_ENTRY, fg=DARK_FG, insertbackground=DARK_FG,
                                                        font=FONT)
        self.descricao_pedido.pack(fill=tk.BOTH, expand=True, pady=5)

        # Lista de pedidos
        cols = [("ID", 50), ("Cliente", 150), ("Data", 120), ("Tipo", 80), 
                ("Qtd Itens", 80), ("Total", 100), ("Motoboy", 120)]
        
        self.tree_pedidos = ttk.Treeview(left_frame, columns=[c[0] for c in cols], show="headings", height=12)
        for col, width in cols:
            self.tree_pedidos.heading(col, text=col)
            self.tree_pedidos.column(col, width=width, anchor='center' if col not in ["Cliente", "Motoboy"] else 'w')
        
        self.tree_pedidos.grid(row=6, column=0, columnspan=2, pady=10, sticky="nsew")
        
        # Vincular evento de seleção para mostrar detalhes
        self.tree_pedidos.bind('<<TreeviewSelect>>', self._mostrar_detalhes_pedido)

        self._atualizar_lista_pedidos()
        self._atualizar_comboboxes()
        self._atualizar_visibilidade_motoboy()

        left_frame.columnconfigure(1, weight=1)
        left_frame.rowconfigure(6, weight=1)

    def _adicionar_produto_pedido(self):
        produto_nome = self.combo_produto.get()
        qtd_str = self.entry_pedido_qtd.get().strip()

        if not all([produto_nome, qtd_str]):
            messagebox.showerror("Erro", "Selecione um produto e informe a quantidade.")
            return

        try:
            qtd = int(qtd_str)
            if qtd <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        produto = next((p for p in self.produtos if p['nome'] == produto_nome), None)
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        # Verifica se o produto já está no pedido
        for item in self.produtos_pedido:
            if item['produto'] == produto_nome:
                item['quantidade'] += qtd
                item['total'] = item['quantidade'] * item['preco_unitario']
                self._atualizar_lista_produtos_pedido()
                self.entry_pedido_qtd.delete(0, tk.END)
                return

        # Adiciona novo produto ao pedido
        self.produtos_pedido.append({
            'produto': produto_nome,
            'quantidade': qtd,
            'preco_unitario': produto['preco'],
            'total': qtd * produto['preco']
        })

        self._atualizar_lista_produtos_pedido()
        self.entry_pedido_qtd.delete(0, tk.END)

    def _atualizar_lista_produtos_pedido(self):
        self._limpar_treeview(self.tree_produtos_pedido)
        for produto in self.produtos_pedido:
            self.tree_produtos_pedido.insert("", "end", values=(
                produto['produto'],
                produto['quantidade'],
                f"{produto['preco_unitario']:.2f}",
                f"{produto['total']:.2f}"
            ))

    def _limpar_pedido(self):
        self.produtos_pedido = []
        self._atualizar_lista_produtos_pedido()
        self.entry_cliente.delete(0, tk.END)
        self.combo_tipo.current(0)
        self._atualizar_visibilidade_motoboy()
        self.descricao_pedido.delete(1.0, tk.END)

    def _adicionar_pedido(self):
        if not self.produtos_pedido:
            messagebox.showerror("Erro", "Adicione pelo menos um produto ao pedido.")
            return

        cliente = self.entry_cliente.get().strip()
        tipo = self.combo_tipo.get()
        
        # Motoboy só é obrigatório para iFood e Robô
        motoboy = self.combo_motoboy.get() if tipo in ['iFood', 'Robô'] else None
        if tipo in ['iFood', 'Robô'] and not motoboy:
            messagebox.showerror("Erro", "Selecione um motoboy para este tipo de pedido.")
            return

        if not cliente:
            messagebox.showerror("Erro", "Informe o nome do cliente.")
            return

        # Verifica estoque para todos os produtos
        for item in self.produtos_pedido:
            produto = next((p for p in self.produtos if p['nome'] == item['produto']), None)
            if not produto:
                messagebox.showerror("Erro", f"Produto {item['produto']} não encontrado.")
                return
                
            if produto['quantidade'] < item['quantidade']:
                messagebox.showerror("Erro", 
                    f"Estoque insuficiente para {item['produto']}. Disponível: {produto['quantidade']}")
                return

        # Busca motoboy se necessário
        motoboy_obj = None
        if motoboy:
            motoboy_obj = next((m for m in self.motoboys if m['nome'] == motoboy), None)
            if not motoboy_obj:
                messagebox.showerror("Erro", "Motoboy não encontrado.")
                return

        # Atualiza estoque
        for item in self.produtos_pedido:
            produto = next((p for p in self.produtos if p['nome'] == item['produto']), None)
            if produto:
                produto['quantidade'] -= item['quantidade']

        DataManager.salvar(DADOS['produtos'], self.produtos)

        # Calcula totais
        total_pedido = sum(item['total'] for item in self.produtos_pedido)
        if tipo == 'iFood':
            total_pedido = round(total_pedido * (1 + PERCENTUAL_IFOOD), 2)

        # Gera ID único para o pedido
        pedido_id = max([p.get('id', 0) for p in self.pedidos] + [0]) + 1

        # Cria pedido
        pedido = {
            'id': pedido_id,
            'cliente': cliente,
            'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'tipo': tipo,
            'motoboy': motoboy if motoboy else "Retirada na Loja",
            'total': total_pedido,
            'produtos': self.produtos_pedido.copy(),
            'qtd_itens': sum(item['quantidade'] for item in self.produtos_pedido)
        }

        self.pedidos.append(pedido)
        DataManager.salvar(DADOS['pedidos'], self.pedidos)
        
        # Atualiza interfaces
        self._atualizar_lista_pedidos()
        self._atualizar_lista_produtos()
        self._limpar_pedido()

    def _mostrar_detalhes_pedido(self, event):
        selecionado = self.tree_pedidos.selection()
        if not selecionado:
            return
            
        item = self.tree_pedidos.item(selecionado)
        pedido_id = item['values'][0]
        
        pedido = next((p for p in self.pedidos if p.get('id') == pedido_id), None)
        if not pedido:
            return
            
        # Limpa a descrição anterior
        self.descricao_pedido.delete(1.0, tk.END)
        
        # Monta a descrição do pedido
        descricao = f"Pedido #{pedido_id}\n"
        descricao += f"Cliente: {pedido['cliente']}\n"
        descricao += f"Data: {pedido['data']}\n"
        descricao += f"Tipo: {pedido['tipo']}\n"
        descricao += f"Motoboy: {pedido['motoboy']}\n"
        descricao += "\nItens do Pedido:\n"
        descricao += "-" * 50 + "\n"
        
        for produto in pedido['produtos']:
            descricao += f"{produto['produto']} - {produto['quantidade']} x R$ {produto['preco_unitario']:.2f} = R$ {produto['total']:.2f}\n"
        
        descricao += "-" * 50 + "\n"
        descricao += f"Total do Pedido: R$ {pedido['total']:.2f}"
        
        self.descricao_pedido.insert(tk.END, descricao)

    def _atualizar_lista_pedidos(self):
        self._limpar_treeview(self.tree_pedidos)
        for p in sorted(self.pedidos, key=lambda x: x.get('id', 0), reverse=True):
            self.tree_pedidos.insert("", "end", values=(
                p.get('id', ''),
                p.get('cliente', ''),
                p['data'],
                p['tipo'],
                p['qtd_itens'],
                f"{p['total']:.2f}",
                p['motoboy']
            ))

    def _editar_pedido(self):
        selecionado = self.tree_pedidos.selection()
        if not selecionado:
            return
            
        item = self.tree_pedidos.item(selecionado)
        pedido_id = item['values'][0]
        
        pedido = next((p for p in self.pedidos if p.get('id') == pedido_id), None)
        if not pedido:
            return
            
        # Devolve os produtos ao estoque
        for produto_pedido in pedido['produtos']:
            produto = next((p for p in self.produtos if p['nome'] == produto_pedido['produto']), None)
            if produto:
                produto['quantidade'] += produto_pedido['quantidade']
        
        DataManager.salvar(DADOS['produtos'], self.produtos)
        
        # Preenche o formulário com os dados do pedido
        self._limpar_pedido()
        self.entry_cliente.insert(0, pedido['cliente'])
        self.combo_tipo.set(pedido['tipo'])
        
        if pedido['tipo'] in ['iFood', 'Robô']:
            self.combo_motoboy.set(pedido['motoboy'])
        
        # Adiciona os produtos ao pedido temporário
        self.produtos_pedido = pedido['produtos'].copy()
        self._atualizar_lista_produtos_pedido()
        
        # Remove o pedido antigo
        self.pedidos = [p for p in self.pedidos if p.get('id') != pedido_id]
        DataManager.salvar(DADOS['pedidos'], self.pedidos)
        
        # Atualiza as listas
        self._atualizar_lista_pedidos()
        self._atualizar_lista_produtos()

    def _excluir_pedido(self):
        selecionado = self.tree_pedidos.selection()
        if not selecionado:
            return
            
        item = self.tree_pedidos.item(selecionado)
        pedido_id = item['values'][0]
        
        pedido = next((p for p in self.pedidos if p.get('id') == pedido_id), None)
        if not pedido:
            return
            
        if messagebox.askyesno("Confirmar", f"Excluir este pedido?"):
            # Devolve os produtos ao estoque
            for produto_pedido in pedido['produtos']:
                produto = next((p for p in self.produtos if p['nome'] == produto_pedido['produto']), None)
                if produto:
                    produto['quantidade'] += produto_pedido['quantidade']
            
            DataManager.salvar(DADOS['produtos'], self.produtos)
            
            # Remove o pedido
            self.pedidos = [p for p in self.pedidos if p.get('id') != pedido_id]
            DataManager.salvar(DADOS['pedidos'], self.pedidos)
            
            # Atualiza as listas
            self._atualizar_lista_pedidos()
            self._atualizar_lista_produtos()
            self.descricao_pedido.delete(1.0, tk.END)

    # ... (outros métodos permanecem os mesmos) ...

if __name__ == "__main__":
    app = App()
    app.mainloop()