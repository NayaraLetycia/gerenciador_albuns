import tkinter as tk
from tkinter import ttk, messagebox
from metal_archives_album_scraper import preencher_planilha

class MetalArchivesGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Metal Archives Album Scraper')
        self.geometry('500x400')
        self.configure(bg='#23272a')
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#23272a', foreground='#e1b382', font=('Segoe UI', 12, 'bold'))
        style.configure('TButton', background='#e1b382', foreground='#23272a', font=('Segoe UI', 11, 'bold'))
        style.configure('TEntry', font=('Segoe UI', 11))

        ttk.Label(self, text='Nome da Banda:').pack(pady=(20, 5))
        self.banda_entry = ttk.Entry(self, width=35)
        self.banda_entry.pack(pady=5)

        ttk.Label(self, text='Nome do Álbum:').pack(pady=5)
        self.album_entry = ttk.Entry(self, width=35)
        self.album_entry.pack(pady=5)

        ttk.Label(self, text='Ano de Lançamento:').pack(pady=5)
        self.ano_entry = ttk.Entry(self, width=35)
        self.ano_entry.pack(pady=5)

        self.status_label = ttk.Label(self, text='', font=('Segoe UI', 10))
        self.status_label.pack(pady=10)

        ttk.Button(self, text='Buscar e Preencher Planilha', command=self.buscar_album).pack(pady=20)

    def buscar_album(self):
        banda = self.banda_entry.get().strip()
        album = self.album_entry.get().strip()
        ano = self.ano_entry.get().strip()
        if not banda or not album or not ano:
            messagebox.showerror('Erro', 'Preencha todos os campos!')
            return
        self.status_label.config(text='Buscando informações...')
        self.update_idletasks()
        try:
            preencher_planilha(banda, album, ano)
            self.status_label.config(text='Planilha atualizada com sucesso!')
        except Exception as e:
            self.status_label.config(text='Erro ao buscar informações.')
            messagebox.showerror('Erro', str(e))

if __name__ == '__main__':
    app = MetalArchivesGUI()
    app.mainloop()
