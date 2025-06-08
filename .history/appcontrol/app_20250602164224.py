import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Teste de Motoboy")
        self.geometry("400x300")

        self.entry_motoboy_nome = ttk.Entry(self)
        self.entry_motoboy_nome.pack(pady=10)

        self.entry_motoboy_valor = ttk.Entry(self)
        self.entry_motoboy_valor.pack(pady=10)

        self.btn_adicionar = ttk.Button(self, text="Adicionar Motoboy", command=self._adicionar_motoboy)
        self.btn_adicionar.pack(pady=10)

    def _adicionar_motoboy(self):
        nome = self.entry_motoboy_nome.get().strip()
        valor = self.entry_motoboy_valor.get().strip()

        if not nome or not valor:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        try:
            valor = float(valor)
            if valor < 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Valor inválido.")
            return

        messagebox.showinfo("Sucesso", f"Motoboy '{nome}' com valor {valor:.2f} adicionado.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
