import customtkinter as ctk
from datetime import datetime

class ScrollableTableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, product_entrys, sells, **kwargs):
        super().__init__(master, **kwargs)

        self.product_entrys = product_entrys
        self.sells = sells

        self.create_table()

    def create_table(self):
        # Criar uma lista única com entrada/saída indicada pelo valor
        combined_list = []

        # Adicionando entradas
        for product in self.product_entrys:
            product_copy = product.copy()  # Fazendo uma cópia para evitar alterações indesejadas na lista original
            product_copy['price'] *= -1
            combined_list.append(product_copy)

        # Adicionando saídas
        for sell in self.sells:
            combined_list.append(sell)

        # Ordenar a lista combinada pela data do recente para o antigo
        combined_list.sort(key=lambda x: datetime.strptime(x.get("date", "1900-01-01"), "%Y-%m-%d"), reverse=True)

        # Cabeçalhos da tabela
        headers = ("name", "price", "quantity", "details", "date")
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self, text=header, anchor="center", font=ctk.CTkFont(size=12))
            label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

        # Dados da tabela
        for row, item in enumerate(combined_list, start=1):
            for col, header in enumerate(headers):
                if header == "price":
                    if item["price"] < 0:
                        value_text = "-{:.2f}".format(abs(item.get(header, 0)))
                        fg_color = "red"
                    else:
                        value_text = "+{:.2f}".format(item.get(header, 0))
                        fg_color = "green"
                elif header == "date":
                    value_text = datetime.strptime(item.get(header, "1900-01-01"), "%Y-%m-%d").strftime("%d/%m/%Y")
                    fg_color = None
                else:
                    value_text = str(item.get(header, ""))
                    fg_color = None

                label = ctk.CTkLabel(self, text=value_text, anchor="center", fg_color=fg_color)
                label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Configurar redimensionamento das células
        for i in range(len(headers)):
            self.grid_columnconfigure(i, weight=1)

        # Configurar redimensionamento da tabela
        self.grid_rowconfigure(0, weight=1)
