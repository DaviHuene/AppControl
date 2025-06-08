import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

VALOR_MOTOBOY = 5.00  # custo fixo por produto para motoboy

class SistemaVendas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Vendas")

        # Dados na memória
        self.produtos = []  # lista de dicts: {'nome', 'preco', 'estoque'}
        self.motoboys = []  # lista de nomes
        self.pedidos = []   # lista de dicts: {'data', 'tipo', 'produto', 'quantidade', 'total', 'motoboy'}

        self.abas = ttk.Notebook(root)
        self.abas.pack(fill="both", expand=True)

        self._criar_aba_produtos()
        self._criar_aba_motoboys()
        self._criar_aba_pedidos()
        self._criar_aba_financeiro()
        self._criar_aba_relatorios()

    # ----- Aba Produtos -----
    def _criar_aba_produtos(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Produtos")

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
        self.entry_prod_nome = ttk.Entry(frame, width=30)
        self.entry_prod_nome.grid(row=0, column=1, pady=5, sticky="w")

        ttk.Label(frame, text="Preço:").grid(row=1, column=0, sticky="w")
        self.entry_prod_preco = ttk.Entry(frame, width=30)
        self.entry_prod_preco.grid(row=1, column=1, pady=5, sticky="w")

        ttk.Label(frame, text="Estoque:").grid(row=2, column=0, sticky="w")
        self.entry_prod_estoque = ttk.Entry(frame, width=30)
        self.entry_prod_estoque.grid(row=2, column=1, pady=5, sticky="w")

        ttk.Button(frame, text="Adicionar Produto", command=self._adicionar_produto).grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        self.tree_produtos = ttk.Treeview(frame, columns=("Preço", "Estoque"), show="headings", height=8)
        self.tree_produtos.heading("Preço", text="Preço (R$)")
        self.tree_produtos.heading("Estoque", text="Estoque")
        self.tree_produtos.grid(row=4, column=0, columnspan=2, sticky="nsew")
        frame.rowconfigure(4, weight=1)
        frame.columnconfigure(1, weight=1)

    def _adicionar_produto(self):
        nome = self.entry_prod_nome.get().strip()
        preco = self.entry_prod_preco.get().strip().replace(",", ".")
        estoque = self.entry_prod_estoque.get().strip()

        if not nome or not preco or not estoque:
            messagebox.showerror("Erro", "Preencha todos os campos de produto.")
            return
        try:
            preco = float(preco)
            estoque = int(estoque)
        except:
            messagebox.showerror("Erro", "Preço deve ser número decimal e estoque um inteiro.")
            return

        # Verifica se produto já existe
        for p in self.produtos:
            if p['nome'].lower() == nome.lower():
                messagebox.showerror("Erro", "Produto já cadastrado.")
                return

        self.produtos.append({'nome': nome, 'preco': preco, 'estoque': estoque})
        self._atualizar_lista_produtos()

        self.entry_prod_nome.delete(0, tk.END)
        self.entry_prod_preco.delete(0, tk.END)
        self.entry_prod_estoque.delete(0, tk.END)

    def _atualizar_lista_produtos(self):
        for i in self.tree_produtos.get_children():
            self.tree_produtos.delete(i)
        for p in self.produtos:
            self.tree_produtos.insert("", tk.END, values=(p['nome'], f"{p['preco']:.2f}", p['estoque']))

    # ----- Aba Motoboys -----
    def _criar_aba_motoboys(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Motoboys")

        ttk.Label(frame, text="Nome do Motoboy:").grid(row=0, column=0, sticky="w")
        self.entry_motoboy_nome = ttk.Entry(frame, width=30)
        self.entry_motoboy_nome.grid(row=0, column=1, pady=5, sticky="w")

        ttk.Button(frame, text="Adicionar Motoboy", command=self._adicionar_motoboy).grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        self.list_motoboys = tk.Listbox(frame, height=8)
        self.list_motoboys.grid(row=2, column=0, columnspan=2, sticky="nsew")
        frame.rowconfigure(2, weight=1)
        frame.columnconfigure(1, weight=1)

    def _adicionar_motoboy(self):
        nome = self.entry_motoboy_nome.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Digite o nome do motoboy.")
            return
        if nome in self.motoboys:
            messagebox.showerror("Erro", "Motoboy já cadastrado.")
            return
        self.motoboys.append(nome)
        self._atualizar_lista_motoboys()
        self.entry_motoboy_nome.delete(0, tk.END)

    def _atualizar_lista_motoboys(self):
        self.list_motoboys.delete(0, tk.END)
        for m in self.motoboys:
            self.list_motoboys.insert(tk.END, m)

    # ----- Aba Pedidos -----
    def _criar_aba_pedidos(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Pedidos")

        ttk.Label(frame, text="Data (DD/MM/AAAA):").grid(row=0, column=0, sticky="w")
        self.entry_pedido_data = ttk.Entry(frame, width=20)
        self.entry_pedido_data.grid(row=0, column=1, pady=5, sticky="w")
        self.entry_pedido_data.insert(0, datetime.now().strftime("%d/%m/%Y"))

        ttk.Label(frame, text="Tipo:").grid(row=1, column=0, sticky="w")
        self.combo_pedido_tipo = ttk.Combobox(frame, values=["Balcão", "Delivery"], state="readonly", width=18)
        self.combo_pedido_tipo.grid(row=1, column=1, pady=5, sticky="w")
        self.combo_pedido_tipo.current(0)

        ttk.Label(frame, text="Produto:").grid(row=2, column=0, sticky="w")
        self.combo_pedido_produto = ttk.Combobox(frame, values=[], state="readonly", width=30)
        self.combo_pedido_produto.grid(row=2, column=1, pady=5, sticky="w")

        ttk.Label(frame, text="Quantidade:").grid(row=3, column=0, sticky="w")
        self.entry_pedido_qtd = ttk.Entry(frame, width=20)
        self.entry_pedido_qtd.grid(row=3, column=1, pady=5, sticky="w")
        self.entry_pedido_qtd.insert(0, "1")

        ttk.Label(frame, text="Motoboy:").grid(row=4, column=0, sticky="w")
        self.combo_pedido_motoboy = ttk.Combobox(frame, values=[], state="readonly", width=30)
        self.combo_pedido_motoboy.grid(row=4, column=1, pady=5, sticky="w")

        ttk.Button(frame, text="Adicionar Pedido", command=self._adicionar_pedido).grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        self.tree_pedidos = ttk.Treeview(frame, columns=("Data", "Tipo", "Produto", "Qtd", "Total", "Motoboy"), show="headings", height=10)
        for col in ("Data", "Tipo", "Produto", "Qtd", "Total", "Motoboy"):
            self.tree_pedidos.heading(col, text=col)
        self.tree_pedidos.grid(row=6, column=0, columnspan=2, sticky="nsew")
        frame.rowconfigure(6, weight=1)
        frame.columnconfigure(1, weight=1)

        ttk.Button(frame, text="Remover Pedido Selecionado", command=self._remover_pedido).grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

        self._atualizar_combo_produtos()
        self._atualizar_combo_motoboys()

    def _atualizar_combo_produtos(self):
        nomes = [p['nome'] for p in self.produtos]
        self.combo_pedido_produto['values'] = nomes
        if nomes:
            self.combo_pedido_produto.current(0)
        else:
            self.combo_pedido_produto.set("")

    def _atualizar_combo_motoboys(self):
        self.combo_pedido_motoboy['values'] = self.motoboys
        if self.motoboys:
            self.combo_pedido_motoboy.current(0)
        else:
            self.combo_pedido_motoboy.set("")

    def _adicionar_pedido(self):
        data = self.entry_pedido_data.get().strip()
        tipo = self.combo_pedido_tipo.get()
        produto_nome = self.combo_pedido_produto.get()
        qtd = self.entry_pedido_qtd.get().strip()
        motoboy = self.combo_pedido_motoboy.get()

        if not data or not produto_nome or not qtd or not motoboy:
            messagebox.showerror("Erro", "Preencha todos os campos do pedido.")
            return

        try:
            data_dt = datetime.strptime(data, "%d/%m/%Y")
        except:
            messagebox.showerror("Erro", "Data inválida. Use DD/MM/AAAA.")
            return

        try:
            qtd = int(qtd)
            if qtd <= 0:
                raise ValueError()
        except:
            messagebox.showerror("Erro", "Quantidade deve ser um inteiro positivo.")
            return

        # Buscar produto para preço e estoque
        produto = next((p for p in self.produtos if p['nome'] == produto_nome), None)
        if produto is None:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        if produto['estoque'] < qtd:
            messagebox.showerror("Erro", f"Estoque insuficiente. Estoque atual: {produto['estoque']}")
            return

        total = produto['preco'] * qtd

        # Atualizar estoque
        produto['estoque'] -= qtd
        self._atualizar_lista_produtos()

        pedido = {
            'data': data,
            'tipo': tipo,
            'produto': produto_nome,
            'quantidade': qtd,
            'total': total,
            'motoboy': motoboy
        }
        self.pedidos.append(pedido)
        self._atualizar_lista_pedidos()
        self._atualizar_financeiro()

        # Limpar campos quantidade e manter outros
        self.entry_pedido_qtd.delete(0, tk.END)
        self.entry_pedido_qtd.insert(0, "1")

    def _atualizar_lista_pedidos(self):
        for i in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(i)
        for p in self.pedidos:
            self.tree_pedidos.insert("", tk.END, values=(p['data'], p['tipo'], p['produto'], p['quantidade'], f"{p['total']:.2f}", p['motoboy']))

    def _remover_pedido(self):
        selecionado = self.tree_pedidos.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um pedido para remover.")
            return
        idx = self.tree_pedidos.index(selecionado[0])
        pedido = self.pedidos.pop(idx)

        # Devolver quantidade ao estoque
        produto = next((p for p in self.produtos if p['nome'] == pedido['produto']), None)
        if produto:
            produto['estoque'] += pedido['quantidade']
            self._atualizar_lista_produtos()

        self._atualizar_lista_pedidos()
        self._atualizar_financeiro()

    # ----- Aba Financeiro -----
    def _criar_aba_financeiro(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Financeiro")

        self.label_receita = ttk.Label(frame, text="Receita Total: R$ 0.00", font=("Arial", 12, "bold"))
        self.label_receita.pack(pady=10)

        self.label_gastos = ttk.Label(frame, text=f"Gastos com Motoboys: R$ 0.00", font=("Arial", 12, "bold"))
        self.label_gastos.pack(pady=10)

        self.label_lucro = ttk.Label(frame, text="Lucro Líquido: R$ 0.00", font=("Arial", 12, "bold"))
        self.label_lucro.pack(pady=10)

    def _atualizar_financeiro(self):
        receita_total = sum(p['total'] for p in self.pedidos)
        gastos_motoboy = sum(p['quantidade'] * VALOR_MOTOBOY for p in self.pedidos)
        lucro_liquido = receita_total - gastos_motoboy

        self.label_receita.config(text=f"Receita Total: R$ {receita_total:.2f}")
        self.label_gastos.config(text=f"Gastos com Motoboys: R$ {gastos_motoboy:.2f}")
        self.label_lucro.config(text=f"Lucro Líquido: R$ {lucro_liquido:.2f}")

    # ----- Aba Relatórios -----
    def _criar_aba_relatorios(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Relatórios")

        ttk.Label(frame, text="Período Início (DD/MM/AAAA):").grid(row=0, column=0, sticky="w")
        self.entry_rel_inicio = ttk.Entry(frame, width=15)
        self.entry_rel_inicio.grid(row=0, column=1, pady=5, sticky="w")

        ttk.Label(frame, text="Período Fim (DD/MM/AAAA):").grid(row=1, column=0, sticky="w")
        self.entry_rel_fim = ttk.Entry(frame, width=15)
        self.entry_rel_fim.grid(row=1, column=1, pady=5, sticky="w")

        ttk.Label(frame, text="Motoboy:").grid(row=2, column=0, sticky="w")
        self.combo_rel_motoboys = ttk.Combobox(frame, values=["Todos"] + self.motoboys, state='readonly', width=30)
        self.combo_rel_motoboys.grid(row=2, column=1, pady=5, sticky="w")
        self.combo_rel_motoboys.current(0)

        ttk.Button(frame, text="Gerar Relatório", command=self._gerar_relatorio).grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        # Área do relatório
        self.text_relatorio = tk.Text(frame, height=20, width=70)
        self.text_relatorio.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

    def _gerar_relatorio(self):
        inicio = self.entry_rel_inicio.get().strip()
        fim = self.entry_rel_fim.get().strip()
        motoboy = self.combo_rel_motoboys.get()

        try:
            dt_inicio = datetime.strptime(inicio, "%d/%m/%Y") if inicio else None
            dt_fim = datetime.strptime(fim, "%d/%m/%Y") if fim else None
        except:
            messagebox.showerror("Erro", "Datas inválidas. Use DD/MM/AAAA.")
            return

        pedidos_filtrados = self.pedidos

        if dt_inicio:
            pedidos_filtrados = [p for p in pedidos_filtrados if datetime.strptime(p['data'], "%d/%m/%Y") >= dt_inicio]
        if dt_fim:
            pedidos_filtrados = [p for p in pedidos_filtrados if datetime.strptime(p['data'], "%d/%m/%Y") <= dt_fim]
        if motoboy != "Todos":
            pedidos_filtrados = [p for p in pedidos_filtrados if p['motoboy'] == motoboy]

        total_vendido = sum(p['total'] for p in pedidos_filtrados)
        total_qtd = sum(p['quantidade'] for p in pedidos_filtrados)

        rel_texto = f"Relatório de Pedidos\n\n"
        rel_texto += f"Período: {inicio or 'Início'} até {fim or 'Fim'}\n"
        rel_texto += f"Motoboy: {motoboy}\n"
        rel_texto += f"Total Vendido: R$ {total_vendido:.2f}\n"
        rel_texto += f"Quantidade Total de Produtos: {total_qtd}\n\n"
        rel_texto += "Detalhes dos Pedidos:\n"
        for p in pedidos_filtrados:
            rel_texto += f"- {p['data']} | {p['tipo']} | {p['produto']} | Qtd: {p['quantidade']} | R$ {p['total']:.2f} | Motoboy: {p['motoboy']}\n"

        self.text_relatorio.delete('1.0', tk.END)
        self.text_relatorio.insert(tk.END, rel_texto)


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaVendas(root)
    root.geometry("800x600")
    root.mainloop()
