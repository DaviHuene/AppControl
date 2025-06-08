import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Exemplo Pedidos")

        # Dados exemplo de pedidos - idealmente você vai preencher isso com seus dados reais
        self.pedidos = [
            {
                'data': '2025-06-01',
                'produto': 'Pizza',
                'quantidade': 2,
                'preco_unitario': 25.50,
                'motoboy': 'João',
                'valor_entrega': 5.00,
                'total': 56.00,
                'lucro': 15.00
            },
            {
                'data': '2025-06-02',
                'produto': 'Hambúrguer',
                'quantidade': 1,
                'preco_unitario': 18.00,
                'motoboy': 'Maria',
                # 'valor_entrega' ausente para testar o get
                'total': 23.00,
                'lucro': 7.00
            }
        ]

        self._criar_interface()

    def _criar_interface(self):
        # Cria a Treeview com colunas
        self.tree_pedidos = ttk.Treeview(self.root, columns=(
            'data', 'produto', 'quantidade', 'preco_unitario',
            'motoboy', 'valor_entrega', 'total', 'lucro'), show='headings')

        # Definindo os cabeçalhos das colunas
        self.tree_pedidos.heading('data', text='Data')
        self.tree_pedidos.heading('produto', text='Produto')
        self.tree_pedidos.heading('quantidade', text='Quantidade')
        self.tree_pedidos.heading('preco_unitario', text='Preço Unitário')
        self.tree_pedidos.heading('motoboy', text='Motoboy')
        self.tree_pedidos.heading('valor_entrega', text='Valor Entrega')
        self.tree_pedidos.heading('total', text='Total')
        self.tree_pedidos.heading('lucro', text='Lucro')

        self.tree_pedidos.pack(fill=tk.BOTH, expand=True)

        # Atualiza a lista de pedidos inicialmente
        self._atualizar_lista_pedidos()

    def _limpar_treeview(self, treeview):
        # Remove todos os itens da Treeview
        for item in treeview.get_children():
            treeview.delete(item)

    def _atualizar_lista_pedidos(self):
        """
        Atualiza a Treeview da aba Pedidos com os dados da lista self.pedidos.
        Usa valores padrão caso alguma chave esteja faltando em um pedido.
        """
        # Limpa dados antigos
        self._limpar_treeview(self.tree_pedidos)

        for p in self.pedidos:
            data = p.get('data', '')
            produto = p.get('produto', '')
            quantidade = p.get('quantidade', 0)
            preco_unitario = p.get('preco_unitario', 0.0)
            motoboy = p.get('motoboy', '')
            valor_entrega = p.get('valor_entrega', 0.0)
            total = p.get('total', 0.0)
            lucro = p.get('lucro', 0.0)

            preco_unitario_str = f"{preco_unitario:.2f}"
            valor_entrega_str = f"{valor_entrega:.2f}"
            total_str = f"{total:.2f}"
            lucro_str = f"{lucro:.2f}"

            self.tree_pedidos.insert("", "end", values=(
                data,
                produto,
                quantidade,
                preco_unitario_str,
                motoboy,
                valor_entrega_str,
                total_str,
                lucro_str
            ))


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
