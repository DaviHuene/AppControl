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
        self.menu_contexto.add_command(label="Editar", command=self.editar_item_selecionado)
        self.menu_contexto.add_command(label="Excluir", command=self.excluir_item_selecionado)
        self.menu_contexto.add_separator()
        self.menu_contexto.add_command(label="Excluir Selecionados (Massa)", command=self.excluir_selecionados_massa)
        
        self.bind("<Button-3>", self.mostrar_menu_contexto)

    def mostrar_menu_contexto(self, event):
        widget = event.widget
        if isinstance(widget, ttk.Treeview):
            item = widget.identify_row(event.y)
            if item:
                if item not in widget.selection():
                    widget.selection_set(item)
                self.menu_contexto.post(event.x_root, event.y_root)

    def editar_item_selecionado(self):
        widget_focado = self.focus_get()
        
        if widget_focado == self.tree_produtos:
            self._editar_produto()
        elif widget_focado == self.tree_pedidos:
            self._editar_pedido()
        elif widget_focado == self.tree_motoboys:
            self._editar_motoboy()

    def excluir_item_selecionado(self):
        widget_focado = self.focus_get()
        
        if widget_focado == self.tree_produtos:
            self._excluir_produto()
        elif widget_focado == self.tree_pedidos:
            self._excluir_pedido()
        elif widget_focado == self.tree_motoboys:
            self._excluir_motoboy()

    def excluir_selecionados_massa(self):
        widget_focado = self.focus_get()
        
        if widget_focado == self.tree_produtos:
            self._excluir_produtos_massa()
        elif widget_focado == self.tree_pedidos:
            self._excluir_pedidos_massa()
        elif widget_focado == self.tree_motoboys:
            self._excluir_motoboys_massa()

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
        self._atualizar_lista_produtos()

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

        produto_atualizado = False
        for p in self.produtos:
            if p['nome'].lower() == nome.lower():
                p.update({'quantidade': qtd, 'preco': preco})
                produto_atualizado = True
                break
        
        if not produto_atualizado:
            self.produtos.append({'nome': nome, 'quantidade': qtd, 'preco': preco})

        DataManager.salvar(DADOS['produtos'], self.produtos)
        self._atualizar_lista_produtos()
        self._limpar_campos([self.entry_nome, self.entry_qtd, self.entry_preco])
        self._atualizar_comboboxes()

    def _editar_produto(self):
        selecionado = self.tree_produtos.selection()
        if not selecionado:
            return
            
        item = self.tree_produtos.item(selecionado)
        nome = item['values'][0]
        
        produto = next((p for p in self.produtos if p['nome'] == nome), None)
        if produto:
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, produto['nome'])
            self.entry_qtd.delete(0, tk.END)
            self.entry_qtd.insert(0, str(produto['quantidade']))
            self.entry_preco.delete(0, tk.END)
            self.entry_preco.insert(0, str(produto['preco']))

    def _excluir_produtos_massa(self):
        selecionados = self.tree_produtos.selection()
        if not selecionados:
            return
            
        nomes = [self.tree_produtos.item(item)['values'][0] for item in selecionados]
        
        if messagebox.askyesno("Confirmar", f"Excluir {len(nomes)} produto(s) selecionado(s)?"):
            self.produtos = [p for p in self.produtos if p['nome'] not in nomes]
            DataManager.salvar(DADOS['produtos'], self.produtos)
            self._atualizar_lista_produtos()
            self._atualizar_comboboxes()

    def _excluir_produto(self):
        selecionado = self.tree_produtos.selection()
        if not selecionado:
            return
            
        item = self.tree_produtos.item(selecionado)
        nome = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Excluir o produto '{nome}'?"):
            self.produtos = [p for p in self.produtos if p['nome'] != nome]
            DataManager.salvar(DADOS['produtos'], self.produtos)
            self._atualizar_lista_produtos()
            self._atualizar_comboboxes()

    def _atualizar_lista_produtos(self):
        self._limpar_treeview(self.tree_produtos)
        for p in sorted(self.produtos, key=lambda x: x['nome']):
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
        self._atualizar_lista_motoboys()

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(3, weight=1)

    def _editar_motoboy(self):
        selecionado = self.tree_motoboys.selection()
        if not selecionado:
            return
            
        item = self.tree_motoboys.item(selecionado)
        nome = item['values'][0]
        
        motoboy = next((m for m in self.motoboys if m['nome'] == nome), None)
        if motoboy:
            self.entry_motoboy_nome.delete(0, tk.END)
            self.entry_motoboy_nome.insert(0, motoboy['nome'])
            self.entry_motoboy_valor.delete(0, tk.END)
            self.entry_motoboy_valor.insert(0, str(motoboy['valor_por_entrega']))

    def _excluir_motoboy(self):
        selecionado = self.tree_motoboys.selection()
        if not selecionado:
            return
            
        item = self.tree_motoboys.item(selecionado)
        nome = item['values'][0]
        
        usado_em_pedidos = any(p['motoboy'] == nome for p in self.pedidos)
        
        if usado_em_pedidos:
            messagebox.showerror("Erro", "Este motoboy está associado a pedidos e não pode ser excluído.")
            return
            
        if messagebox.askyesno("Confirmar", f"Excluir o motoboy '{nome}'?"):
            self.motoboys = [m for m in self.motoboys if m['nome'] != nome]
            DataManager.salvar(DADOS['motoboys'], self.motoboys)
            self._atualizar_lista_motoboys()
            self._atualizar_comboboxes()

    def _excluir_motoboys_massa(self):
        selecionados = self.tree_motoboys.selection()
        if not selecionados:
            return
            
        nomes = [self.tree_motoboys.item(item)['values'][0] for item in selecionados]
        
        motoboys_em_uso = []
        for nome in nomes:
            if any(p['motoboy'] == nome for p in self.pedidos):
                motoboys_em_uso.append(nome)
        
        if motoboys_em_uso:
            messagebox.showerror("Erro", 
                f"Os seguintes motoboys estão em pedidos e não podem ser excluídos: {', '.join(motoboys_em_uso)}")
            return
            
        if messagebox.askyesno("Confirmar", f"Excluir {len(nomes)} motoboy(s) selecionado(s)?"):
            self.motoboys = [m for m in self.motoboys if m['nome'] not in nomes]
            DataManager.salvar(DADOS['motoboys'], self.motoboys)
            self._atualizar_lista_motoboys()
            self._atualizar_comboboxes()

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

        motoboy_atualizado = False
        for m in self.motoboys:
            if m['nome'].lower() == nome.lower():
                m['valor_por_entrega'] = valor
                motoboy_atualizado = True
                break
        
        if not motoboy_atualizado:
            self.motoboys.append({'nome': nome, 'valor_por_entrega': valor})

        DataManager.salvar(DADOS['motoboys'], self.motoboys)
        self._atualizar_lista_motoboys()
        self._limpar_campos([self.entry_motoboy_nome, self.entry_motoboy_valor])
        self._atualizar_comboboxes()

    def _atualizar_lista_motoboys(self):
        self._limpar_treeview(self.tree_motoboys)
        for m in sorted(self.motoboys, key=lambda x: x['nome']):
            self.tree_motoboys.insert("", "end", values=(
                m['nome'], 
                f"{m['valor_por_entrega']:.2f}"
            ))
            
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

    def _excluir_pedidos_massa(self):
        selecionados = self.tree_pedidos.selection()
        if not selecionados:
            return
            
        pedidos_para_excluir = []
        produtos_para_atualizar = {}
        
        for item in selecionados:
            valores = self.tree_pedidos.item(item)['values']
            pedido_id = valores[0]
            
            pedido = next((p for p in self.pedidos if p.get('id') == pedido_id), None)
            if not pedido:
                continue
                
            pedidos_para_excluir.append(pedido_id)
            
            for produto_pedido in pedido['produtos']:
                produto_nome = produto_pedido['produto']
                quantidade = produto_pedido['quantidade']
                
                if produto_nome in produtos_para_atualizar:
                    produtos_para_atualizar[produto_nome] += quantidade
                else:
                    produtos_para_atualizar[produto_nome] = quantidade
        
        if not messagebox.askyesno("Confirmar", f"Excluir {len(pedidos_para_excluir)} pedido(s) selecionado(s)?"):
            return
        
        for produto_nome, quantidade in produtos_para_atualizar.items():
            produto = next((p for p in self.produtos if p['nome'] == produto_nome), None)
            if produto:
                produto['quantidade'] += quantidade
        
        self.pedidos = [p for p in self.pedidos if p.get('id') not in pedidos_para_excluir]
        
        DataManager.salvar(DADOS['produtos'], self.produtos)
        DataManager.salvar(DADOS['pedidos'], self.pedidos)
        self._atualizar_lista_pedidos()
        self._atualizar_lista_produtos()
        self.descricao_pedido.delete(1.0, tk.END)

    def _atualizar_visibilidade_motoboy(self, event=None):
        tipo = self.combo_tipo.get()
        if tipo == 'Loja':
            self.motoboy_frame.grid_remove()
        else:
            self.motoboy_frame.grid()

    def _criar_aba_financeiro(self):
        frame = ttk.Frame(self.abas, padding=20)
        self.abas.add(frame, text="Financeiro")

        ttk.Label(frame, text="Resumo Financeiro", font=('Segoe UI', 12, 'bold')).pack(pady=10)

        self.lbl_vendas = ttk.Label(frame, text="Total Vendas: R$ 0.00", font=FONT)
        self.lbl_vendas.pack(pady=5)

        self.lbl_motoboys = ttk.Label(frame, text="Total Motoboys: R$ 0.00", font=FONT)
        self.lbl_motoboys.pack(pady=5)

        self.lbl_lucro = ttk.Label(frame, text="Lucro Líquido: R$ 0.00", font=('Segoe UI', 12, 'bold'))
        self.lbl_lucro.pack(pady=15)

        ttk.Button(frame, text="Calcular", command=self._calcular_financeiro).pack(pady=10)

    def _calcular_financeiro(self):
        total_vendas = sum(p['total'] for p in self.pedidos)
        
        total_motoboys = 0
        for p in self.pedidos:
            if p['tipo'] != 'Loja':
                motoboy = next((m for m in self.motoboys if m['nome'] == p['motoboy']), None)
                if motoboy:
                    total_motoboys += motoboy['valor_por_entrega']

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