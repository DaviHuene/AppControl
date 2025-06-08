# Continuação da classe App...

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
                m['valor'] = valor
                break
        else:
            self.motoboys.append({'nome': nome, 'valor': valor})

        DataManager.salvar(DADOS['motoboys'], self.motoboys)
        self._atualizar_lista_motoboys()
        self._limpar_campos([self.entry_motoboy_nome, self.entry_motoboy_valor])

    def _atualizar_lista_motoboys(self):
        self._limpar_treeview(self.tree_motoboys)
        for m in self.motoboys:
            self.tree_motoboys.insert("", "end", values=(m['nome'], f"{m['valor']:.2f}"))

    # --- Aba Pedidos ---
    def _criar_aba_pedidos(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Pedidos")

        # Formulário
        ttk.Label(frame, text="Produto:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_pedido_produto = ttk.Combobox(frame, values=[p['nome'] for p in self.produtos], state='readonly')
        self.combo_pedido_produto.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Quantidade:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_pedido_qtd = ttk.Entry(frame)
        self.entry_pedido_qtd.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Motoboy:").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_pedido_motoboy = ttk.Combobox(frame, values=[m['nome'] for m in self.motoboys], state='readonly')
        self.combo_pedido_motoboy.grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Button(frame, text="Registrar Pedido", command=self._registrar_pedido).grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        # Lista pedidos
        self.tree_pedidos = ttk.Treeview(frame, columns=("Produto", "Qtd", "Valor Unitário", "Motoboy", "Data"), show="headings", height=12)
        for col, width in [("Produto", 250), ("Qtd", 60), ("Valor Unitário", 100), ("Motoboy", 150), ("Data", 140)]:
            self.tree_pedidos.heading(col, text=col)
            self.tree_pedidos.column(col, width=width, anchor='center' if col != "Produto" else 'w')
        self.tree_pedidos.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

        # Configuração grid
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

        self._atualizar_lista_pedidos()

    def _registrar_pedido(self):
        produto_nome = self.combo_pedido_produto.get()
        qtd_str = self.entry_pedido_qtd.get()
        motoboy_nome = self.combo_pedido_motoboy.get()

        if not all([produto_nome, qtd_str, motoboy_nome]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        try:
            qtd = int(qtd_str)
            if qtd <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        produto = next((p for p in self.produtos if p['nome'] == produto_nome), None)
        motoboy = next((m for m in self.motoboys if m['nome'] == motoboy_nome), None)

        if produto is None or motoboy is None:
            messagebox.showerror("Erro", "Produto ou motoboy não encontrado.")
            return

        if produto['quantidade'] < qtd:
            messagebox.showerror("Erro", f"Quantidade em estoque insuficiente (Disponível: {produto['quantidade']})")
            return

        # Atualiza estoque
        produto['quantidade'] -= qtd
        DataManager.salvar(DADOS['produtos'], self.produtos)
        self._atualizar_lista_produtos()

        pedido = {
            'produto': produto_nome,
            'quantidade': qtd,
            'valor_unitario': produto['preco'],
            'motoboy': motoboy_nome,
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.pedidos.append(pedido)
        DataManager.salvar(DADOS['pedidos'], self.pedidos)

        self._atualizar_lista_pedidos()
        self._limpar_campos([self.entry_pedido_qtd])
        self.combo_pedido_produto.set('')
        self.combo_pedido_motoboy.set('')

    def _atualizar_lista_pedidos(self):
        self._limpar_treeview(self.tree_pedidos)
        for ped in self.pedidos:
            self.tree_pedidos.insert("", "end", values=(
                ped['produto'],
                ped['quantidade'],
                f"{ped['valor_unitario']:.2f}",
                ped['motoboy'],
                ped['data']
            ))

    # --- Aba Financeiro ---
    def _criar_aba_financeiro(self):
        frame = ttk.Frame(self.abas, padding=10)
        self.abas.add(frame, text="Financeiro")

        # Botão atualizar relatório
        ttk.Button(frame, text="Atualizar Relatório", command=self._atualizar_relatorio).pack(fill='x', pady=5)

        # Treeview resumo financeiro
        cols = ("Total Bruto", "Comissão iFood (20%)", "Valor iFood", "Total Líquido", "Total Motoboys")
        self.tree_financeiro = ttk.Treeview(frame, columns=cols, show="headings", height=1)
        for col in cols:
            self.tree_financeiro.heading(col, text=col)
            self.tree_financeiro.column(col, width=150, anchor='center')
        self.tree_financeiro.pack(fill='x', pady=10)

        # Treeview pedidos detalhados
        ttk.Label(frame, text="Pedidos Detalhados:").pack(anchor='w')
        cols_ped = ("Produto", "Qtd", "Valor Unitário", "Total Produto", "Motoboy", "Valor Motoboy", "Data")
        self.tree_financeiro_detalhe = ttk.Treeview(frame, columns=cols_ped, show="headings", height=12)
        for col, width in zip(cols_ped, [200, 60, 120, 120, 150, 130, 160]):
            self.tree_financeiro_detalhe.heading(col, text=col)
            self.tree_financeiro_detalhe.column(col, width=width, anchor='center' if col != "Produto" and col != "Motoboy" else 'w')
        self.tree_financeiro_detalhe.pack(fill='both', expand=True, pady=10)

        self._atualizar_relatorio()

    def _atualizar_relatorio(self):
        self._limpar_treeview(self.tree_financeiro)
        self._limpar_treeview(self.tree_financeiro_detalhe)

        total_bruto = sum(p['valor_unitario'] * p['quantidade'] for p in self.pedidos)
        comissao_ifood = total_bruto * PERCENTUAL_IFOOD
        valor_ifood = total_bruto - comissao_ifood
        total_motoboys = 0

        for p in self.pedidos:
            motoboy = next((m for m in self.motoboys if m['nome'] == p['motoboy']), None)
            valor_motoboy = motoboy['valor'] * p['quantidade'] if motoboy else 0
            total_motoboys += valor_motoboy
            total_produto = p['valor_unitario'] * p['quantidade']

            self.tree_financeiro_detalhe.insert("", "end", values=(
                p['produto'],
                p['quantidade'],
                f"{p['valor_unitario']:.2f}",
                f"{total_produto:.2f}",
                p['motoboy'],
                f"{valor_motoboy:.2f}",
                p['data']
            ))

        total_liquido = total_bruto - comissao_ifood - total_motoboys

        self.tree_financeiro.insert("", "end", values=(
            f"R$ {total_bruto:.2f}",
            f"R$ {comissao_ifood:.2f}",
            f"R$ {valor_ifood:.2f}",
            f"R$ {total_liquido:.2f}",
            f"R$ {total_motoboys:.2f}"
        ))

    # --- Helpers ---
    def _limpar_treeview(self, tree):
        for i in tree.get_children():
            tree.delete(i)

    def _limpar_campos(self, widgets):
        for w in widgets:
            w.delete(0, tk.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()