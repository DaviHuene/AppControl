import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

# Configurações de Cores
DARK_BG = '#121212'
DARK_FG = "#FFFB0D"
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
        self._criar_menu_contexto()
        self._criar_interface()

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
        
        # Vincular o menu de contexto a todos os treeviews
        self.bind("<Button-3>", self._mostrar_menu_contexto)

    def _mostrar_menu_contexto(self, event):
        widget = event.widget
        if isinstance(widget, ttk.Treeview):
            item = widget.identify_row(event.y)
            if item:
                # Seleciona o item sob o cursor se não estiver já selecionado
                if item not in widget.selection():
                    widget.selection_set(item)
                self.menu_contexto.post(event.x_root, event.y_root)

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

    def _editar_item_selecionado(self):
        # Verifica qual treeview está com foco
        widget_focado = self.focus_get()
        
        if widget_focado == self.tree_produtos:
            self._editar_produto()
        elif widget_focado == self.tree_pedidos:
            self._editar_pedido()
        elif widget_focado == self.tree_motoboys:
            self._editar_motoboy()

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

    def _excluir_item_selecionado(self):
        widget_focado = self.focus_get()
        
        if widget_focado == self.tree_produtos:
            self._excluir_produto()
        elif widget_focado == self.tree_pedidos:
            self._excluir_pedido()
        elif widget_focado == self.tree_motoboys:
            self._excluir_motoboy()

    def _excluir_selecionados_massa(self):
        widget_focado = self.focus_get()
        
        if widget_focado == self.tree_produtos:
            self._excluir_produtos_massa()
        elif widget_focado == self.tree_pedidos:
            self._excluir_pedidos_massa()
        elif widget_focado == self.tree_motoboys:
            self._excluir_motoboys_massa()

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

    def _excluir_pedidos_massa(self):
        selecionados = self.tree_pedidos.selection()
        if not selecionados:
            return
            
        pedidos_para_excluir = []
        produtos_para_atualizar = {}
        
        # Primeiro coleta todas as informações necessárias
        for item in selecionados:
            valores = self.tree_pedidos.item(item)['values']
            pedido_id = valores[0]
            produto_nome = valores[3]
            quantidade = valores[4]
            
            pedidos_para_excluir.append(pedido_id)
            
            if produto_nome in produtos_para_atualizar:
                produtos_para_atualizar[produto_nome] += quantidade
            else:
                produtos_para_atualizar[produto_nome] = quantidade
        
        if not messagebox.askyesno("Confirmar", f"Excluir {len(pedidos_para_excluir)} pedido(s) selecionado(s)?"):
            return
        
        # Atualiza estoque
        for produto_nome, quantidade in produtos_para_atualizar.items():
            produto = next((p for p in self.produtos if p['nome'] == produto_nome), None)
            if produto:
                produto['quantidade'] += quantidade
        
        # Remove os pedidos
        self.pedidos = [p for p in self.pedidos if p.get('id') not in pedidos_para_excluir]
        
        DataManager.salvar(DADOS['produtos'], self.produtos)
        DataManager.salvar(DADOS['pedidos'], self.pedidos)
        self._atualizar_lista_pedidos()
        self._atualizar_lista_produtos()

    def _excluir_motoboys_massa(self):
        selecionados = self.tree_motoboys.selection()
        if not selecionados:
            return
            
        nomes = [self.tree_motoboys.item(item)['values'][0] for item in selecionados]
        
        # Verifica se algum motoboy está em uso
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
        
        # Verificar se o motoboy está em algum pedido
        usado_em_pedidos = any(p['motoboy'] == nome for p in self.pedidos)
        
        if usado_em_pedidos:
            messagebox.showerror("Erro", "Este motoboy está associado a pedidos e não pode ser excluído.")
            return
            
        if messagebox.askyesno("Confirmar", f"Excluir o motoboy '{nome}'?"):
            self.motoboys = [m for m in self.motoboys if m['nome'] != nome]
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

        # Atualiza ou adiciona motoboy
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

    # Formulário
    ttk.Label(frame, text="Nome do Cliente:").grid(row=0, column=0, sticky="w", pady=5)
    self.entry_cliente = ttk.Entry(frame, width=30)
    self.entry_cliente.grid(row=0, column=1, pady=5, sticky="ew")

    ttk.Label(frame, text="Tipo do Pedido:").grid(row=1, column=0, sticky="w", pady=5)
    self.combo_tipo = ttk.Combobox(frame, values=['Loja', 'iFood', 'Robô'], state="readonly", width=27)
    self.combo_tipo.current(0)
    self.combo_tipo.grid(row=1, column=1, pady=5, sticky="ew")
    self.combo_tipo.bind('<<ComboboxSelected>>', self._atualizar_visibilidade_motoboy)

    ttk.Label(frame, text="Produto:").grid(row=2, column=0, sticky="w", pady=5)
    self.combo_produto = ttk.Combobox(frame, state="readonly", width=27)
    self.combo_produto.grid(row=2, column=1, pady=5, sticky="ew")

    ttk.Label(frame, text="Quantidade:").grid(row=3, column=0, sticky="w", pady=5)
    self.entry_pedido_qtd = ttk.Entry(frame, width=30)
    self.entry_pedido_qtd.grid(row=3, column=1, pady=5, sticky="ew")

    # Frame para motoboy (pode ser escondido)
    self.motoboy_frame = ttk.Frame(frame)
    self.motoboy_frame.grid(row=4, column=0, columnspan=2, sticky="ew")
    
    ttk.Label(self.motoboy_frame, text="Motoboy:").grid(row=0, column=0, sticky="w", pady=5)
    self.combo_motoboy = ttk.Combobox(self.motoboy_frame, state="readonly", width=27)
    self.combo_motoboy.grid(row=0, column=1, pady=5, sticky="ew")

    ttk.Button(frame, text="Adicionar Pedido", 
              command=self._adicionar_pedido).grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

    # Lista de pedidos
    cols = [("ID", 50), ("Cliente", 150), ("Data", 120), ("Tipo", 80), 
            ("Produto", 150), ("Qtd", 60), ("Valor", 100), ("Motoboy", 120), ("Total", 100)]
    
    self.tree_pedidos = ttk.Treeview(frame, columns=[c[0] for c in cols], show="headings", height=12)
    for col, width in cols:
        self.tree_pedidos.heading(col, text=col)
        self.tree_pedidos.column(col, width=width, anchor='center' if col not in ["Cliente", "Produto", "Motoboy"] else 'w')
    
    self.tree_pedidos.grid(row=6, column=0, columnspan=2, pady=10, sticky="nsew")
    self._atualizar_lista_pedidos()

    # Atualizar comboboxes
    self._atualizar_comboboxes()

    # Configuração de grid
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(6, weight=1)
    def _editar_pedido(self):
        selecionado = self.tree_pedidos.selection()
        if not selecionado:
            return
            
        item = self.tree_pedidos.item(selecionado)
        pedido_id = item['values'][0]
        
        pedido = next((p for p in self.pedidos if p.get('id') == pedido_id), None)
        if pedido:
            # Primeiro, devolve o estoque do pedido atual
            produto = next((p for p in self.produtos if p['nome'] == pedido['produto']), None)
            if produto:
                produto['quantidade'] += pedido['quantidade']
                DataManager.salvar(DADOS['produtos'], self.produtos)
            
            # Preenche o formulário com os dados do pedido
            self.combo_tipo.set(pedido['tipo'])
            self.combo_produto.set(pedido['produto'])
            self.entry_pedido_qtd.delete(0, tk.END)
            self.entry_pedido_qtd.insert(0, str(pedido['quantidade']))
            
            if pedido['tipo'] in ['iFood', 'Robô']:
                self.combo_motoboy.set(pedido['motoboy'])
            
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
        produto_nome = item['values'][3]
        quantidade = int(item['values'][4])
        
        pedido = next((p for p in self.pedidos if p.get('id') == pedido_id), None)
        if not pedido:
            return
            
        if messagebox.askyesno("Confirmar", f"Excluir este pedido?"):
            # Devolve o estoque
            produto = next((p for p in self.produtos if p['nome'] == produto_nome), None)
            if produto:
                produto['quantidade'] += quantidade
                DataManager.salvar(DADOS['produtos'], self.produtos)
            
            # Remove o pedido
            self.pedidos = [p for p in self.pedidos if p.get('id') != pedido_id]
            DataManager.salvar(DADOS['pedidos'], self.pedidos)
            
            # Atualiza as listas
            self._atualizar_lista_pedidos()
            self._atualizar_lista_produtos()

    def _atualizar_visibilidade_motoboy(self, event=None):
        tipo = self.combo_tipo.get()
        if tipo == 'Loja':
            self.motoboy_frame.grid_remove()
        else:
            self.motoboy_frame.grid()

    def _adicionar_pedido(self):
        tipo = self.combo_tipo.get()
        produto = self.combo_produto.get()
        qtd_str = self.entry_pedido_qtd.get().strip()
        
        # Motoboy só é obrigatório para iFood e Robô
        motoboy = self.combo_motoboy.get() if tipo in ['iFood', 'Robô'] else None
        if tipo in ['iFood', 'Robô'] and not motoboy:
            messagebox.showerror("Erro", "Selecione um motoboy para este tipo de pedido.")
            return

        if not produto or not qtd_str:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return

        try:
            qtd = int(qtd_str)
            if qtd <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        # Busca produto
        produto_obj = next((p for p in self.produtos if p['nome'] == produto), None)
        if not produto_obj:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return
            
        # Verifica estoque
        if produto_obj['quantidade'] < qtd:
            messagebox.showerror("Erro", f"Estoque insuficiente. Disponível: {produto_obj['quantidade']}")
            return

        # Busca motoboy se necessário
        motoboy_obj = None
        if motoboy:
            motoboy_obj = next((m for m in self.motoboys if m['nome'] == motoboy), None)
            if not motoboy_obj:
                messagebox.showerror("Erro", "Motoboy não encontrado.")
                return

        # Calcula preço (com taxa para iFood)
        preco = produto_obj['preco']
        if tipo == 'iFood':
            preco = round(preco * (1 + PERCENTUAL_IFOOD), 2)

        # Atualiza estoque
        produto_obj['quantidade'] -= qtd
        DataManager.salvar(DADOS['produtos'], self.produtos)

        # Gera ID único para o pedido
        pedido_id = max([p.get('id', 0) for p in self.pedidos] + [0]) + 1

        # Cria pedido
        pedido = {
            'id': pedido_id,
            'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'tipo': tipo,
            'produto': produto,
            'quantidade': qtd,
            'preco_unitario': preco,
            'motoboy': motoboy if motoboy else "Retirada na Loja",
            'total': preco * qtd
        }

        self.pedidos.append(pedido)
        DataManager.salvar(DADOS['pedidos'], self.pedidos)
        self._atualizar_lista_pedidos()
        self._atualizar_lista_produtos()
        self.entry_pedido_qtd.delete(0, tk.END)

    def _atualizar_lista_pedidos(self):
        self._limpar_treeview(self.tree_pedidos)
        for p in sorted(self.pedidos, key=lambda x: x.get('id', 0), reverse=True):
            self.tree_pedidos.insert("", "end", values=(
                p.get('id', ''),
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
            if p['tipo'] != 'Loja':  # Só calcula para pedidos com entrega
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