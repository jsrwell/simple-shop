"""
This module contains the ScrollableTableFrame
class which is a scrollable frame containing a table.
"""
from datetime import datetime
import customtkinter as ctk


class ScrollableTableFrame(ctk.CTkScrollableFrame):
    """A scrollable frame containing a table."""

    def __init__(self, master, product_entrys, app_instance, **kwargs):
        """Initialize the scrollable table frame."""

        super().__init__(master, **kwargs)
        self.product_entrys = product_entrys
        self.create_table(app_instance)

    def create_table(self, app_instance):
        """Create the table."""

        product_entrys = self.product_entrys

        # Sort the combined list by date from recent to old
        product_entrys.sort(key=lambda x: datetime.strptime(
            x.get("date", "1900-01-01"), "%Y-%m-%d"), reverse=True)

        # Table headers
        headers = ("name", "price", "details", "date", "actions")
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                self, text=header, anchor="center", font=ctk.CTkFont(size=12))
            label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

        # Table data
        for row, item in enumerate(product_entrys, start=1):
            for col, header in enumerate(headers):
                if header == "price":
                    if item["price"] < 0:
                        value_text = "-{:.2f}".format(abs(item.get(header, 0)))
                        fg_color = "red"
                    else:
                        value_text = "+{:.2f}".format(item.get(header, 0))
                        fg_color = "green"
                elif header == "date":
                    value_text = datetime.strptime(
                        item.get(header, "1900-01-01"),
                        "%Y-%m-%d").strftime("%d/%m/%Y")
                    fg_color = None

                elif header == "actions":
                    # Add delete button
                    delete_button = ctk.CTkButton(
                        self, text="Delete",
                        command=lambda record_id=item["id"]:
                        app_instance.delete_record_and_redirect(record_id))
                    delete_button.grid(row=row, column=col,
                                       padx=5, pady=5, sticky="nsew")
                    continue

                else:
                    value_text = str(item.get(header, ""))
                    fg_color = None

                label = ctk.CTkLabel(self, text=value_text,
                                     anchor="center", fg_color=fg_color)
                label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Configure cell resizing
        for i in range(len(headers)):
            self.grid_columnconfigure(i, weight=1)

        # Configure table resizing
        self.grid_rowconfigure(0, weight=1)
