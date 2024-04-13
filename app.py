"""
App Main File
"""
# System Imports
import os
from datetime import (
    datetime,
    timedelta,
)

# Third-Party Imports
from tkcalendar import DateEntry
from PIL import Image
import customtkinter as ctk

# Local Imports
from utils.tables import ScrollableTableFrame
from db.database import check_database
from db.handlers import (
    delete_record,
    get_records_by_date_range,
    insert_record,
)

# Check if the database exists and create it if it doesn't
check_database()


class App(ctk.CTk):
    """Main application class."""

    def __init__(self):
        """Initialize the application."""

        super().__init__()

        self.title("Gestão de Estoque")
        self.geometry("1080x720")
        self.center_window()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.load_images()
        self.create_navigation_frame()
        self.create_home_frame()
        self.create_second_frame()
        self.create_third_frame()

        # Set the system color as the default value for the theme
        self.appearance_mode_menu.set("System")

        self.select_frame_by_name("home")

    def center_window(self):
        """Center the application window on the screen."""

        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.winfo_reqwidth()) // 2
        y = (screen_height - self.winfo_reqheight()) // 2
        self.geometry("+{}+{}".format(x, y))

    def load_images(self):
        """Load images for the application."""

        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(
            image_path, "tkinter.png")), size=(26, 26))
        self.large_test_image = ctk.CTkImage(Image.open(
            os.path.join(image_path, "manager.png")), size=(1000, 200))
        self.home_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "home_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "home_light.png")),
            size=(20, 20))
        self.chat_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
            size=(20, 20))
        self.add_user_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(
                image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(
                image_path, "add_user_light.png")), size=(20, 20))

    def create_navigation_frame(self):
        """Create the navigation frame."""

        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(
            self.navigation_frame, text="  Controle", image=self.logo_image,
            compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40,
            border_spacing=10, text="Painel Principal",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40,
            border_spacing=10, text="Venda/Gasto",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.chat_image, anchor="w",
            command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40,
            border_spacing=10, text="Relatórios",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_user_image, anchor="w",
            command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        # Set the system color as the default value for the theme selection
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.navigation_frame, values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(
            row=6, column=0, padx=20, pady=20, sticky="s")

    def create_home_frame(self):
        """Create the home frame."""
        self.home_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # Imagem
        self.home_frame_large_image_label = ctk.CTkLabel(
            self.home_frame, text="",
            image=self.large_test_image,
            corner_radius=50)
        self.home_frame_large_image_label.grid(
            row=0, column=0, columnspan=4, padx=20, pady=10)

        # Labels
        start_label = ctk.CTkLabel(self.home_frame, text="Início da Pesquisa:")
        start_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="e")

        end_label = ctk.CTkLabel(self.home_frame, text="Final da Pesquisa:")
        end_label.grid(row=1, column=2, padx=(10, 20), pady=10, sticky="e")

        # Date inputs
        self.start_date = DateEntry(self.home_frame, date_pattern="dd/mm/yyyy")
        self.start_date.set_date(datetime.now() - timedelta(days=30))
        self.start_date.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.start_date.bind("<<DateEntrySelected>>", self.filter_records)

        self.end_date = DateEntry(self.home_frame, date_pattern="dd/mm/yyyy")
        self.end_date.set_date(datetime.now())
        self.end_date.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        self.end_date.bind("<<DateEntrySelected>>", self.filter_records)

        # Configure column weights to make labels and entries equal in width
        self.home_frame.grid_columnconfigure(1, weight=1)
        self.home_frame.grid_columnconfigure(3, weight=1)

        # Initial data filter
        self.filter_records()

    def filter_records(self, event=None):
        """Filter records based on the selected date range."""
        start_date = self.start_date.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date.get_date().strftime("%Y-%m-%d")
        data = get_records_by_date_range(start_date, end_date)

        # Destroy and recreate the scrollable table frame
        if hasattr(self, "scrollable_table_frame"):
            self.scrollable_table_frame.destroy()

        self.scrollable_table_frame = ScrollableTableFrame(
            master=self.home_frame, product_entrys=data, app_instance=self)
        self.scrollable_table_frame.grid(
            row=2, column=0, columnspan=4, padx=20, pady=(0, 10), sticky="nsew")

        # Configure the last row to expand when the window is resized
        self.home_frame.grid_rowconfigure(2, weight=1)

    def create_second_frame(self):
        """Create the second frame."""

        self.second_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")

        # Button to perform a new sale
        new_sale_button = ctk.CTkButton(self.second_frame,
                                        text="Nova Venda",
                                        command=self.new_sale_button_event,
                                        width=20,
                                        height=6,
                                        font=ctk.CTkFont(size=20),
                                        fg_color="green",
                                        hover_color=(
                                             "darkgreen", "darkgreen"),
                                        border_spacing=10)
        new_sale_button.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Button to perform stock entry
        stock_entry_button = ctk.CTkButton(
            self.second_frame,
            text="Novo Gasto",
            command=self.stock_entry_button_event,
            width=20,
            height=6,
            font=ctk.CTkFont(size=20),
            fg_color="red",
            hover_color=(
                "darkred", "darkred"),
            border_spacing=10)
        stock_entry_button.grid(
            row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Configure cell resizing
        self.second_frame.grid_rowconfigure(0, weight=1)
        self.second_frame.grid_rowconfigure(1, weight=1)
        self.second_frame.grid_columnconfigure(0, weight=1)

    def new_sale_button_event(self):
        """Event handler for the new sale button."""

        self.create_data_entry_frame("Nova Venda")

    def stock_entry_button_event(self):
        """Event handler for the stock entry button."""

        self.create_data_entry_frame("Novo Gasto", input=False)

    def create_data_entry_frame(self, title, input=True):
        """Create a frame for data entry."""

        # Data Frame Creation
        self.data_entry_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.data_entry_frame.grid(row=0, column=1, sticky="nsew")

        # Adicionando uma linha extra para os botões
        self.data_entry_frame.grid_rowconfigure(6, weight=1)

        # Title
        title_label = ctk.CTkLabel(
            self.data_entry_frame,
            text=title, font=ctk.CTkFont(size=15, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Labels
        labels = ["Nome do Produto:", "Valor:", "Detalhes:", "Data:"]
        entries = {}
        row = 1
        for label_text in labels:
            label = ctk.CTkLabel(self.data_entry_frame, text=label_text)
            label.grid(row=row, column=0, padx=10, pady=5, sticky="e")

            if label_text == "Data:":
                date_entry = DateEntry(
                    self.data_entry_frame, date_pattern="dd/mm/yyyy")
                date_entry.set_date(datetime.now())
                date_entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
                entries["date"] = date_entry
            else:
                entry = ctk.CTkEntry(self.data_entry_frame)
                entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
                entries[label_text.strip(" :")] = entry

            row += 1

        # Confirm Button
        confirm_button = ctk.CTkButton(
            self.data_entry_frame, text="Confirmar",
            command=lambda: self.save_data(entries, input=input))
        confirm_button.grid(row=row, column=0,
                            pady=10)

        # Cancel Button
        cancel_button = ctk.CTkButton(
            self.data_entry_frame, text="Cancelar",
            command=self.cancel_data_entry)
        cancel_button.grid(row=row, column=1, pady=10)

    def cancel_data_entry(self):
        """Cancel data entry."""

        self.data_entry_frame.destroy()

    def save_data(self, entries, input=True):
        """Save data to the database."""

        data_for_save = {}

        # Clean Data
        for label, entry in entries.items():
            if entry.get().strip() == "":
                return

            if label == "Valor":
                try:
                    price = float(entry.get())
                    if not input:
                        price = -price
                    data_for_save['price'] = price
                except ValueError:
                    return

            elif label == "date":
                date_obj = datetime.strptime(entry.get(), "%d/%m/%Y")
                date_str = date_obj.strftime("%Y-%m-%d")
                data_for_save['date'] = date_str

            elif label == "Nome do Produto":
                data_for_save['name'] = entry.get()

            elif label == "Detalhes":
                data_for_save['details'] = entry.get()

        result = insert_record(
            name=data_for_save['name'],
            price=data_for_save['price'],
            details=data_for_save['details'],
            date=data_for_save['date']
        )

        if result:
            print('Salvo com sucesso!')
            self.data_entry_frame.destroy()
        else:
            print("Erro ao salvar")

    def create_third_frame(self):
        """Create the third frame."""

        self.third_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")

        # Add content for the third frame here

    def select_frame_by_name(self, name):
        """Select a frame by its name."""

        frames = {"home": self.home_frame,
                  "frame_2": self.second_frame,
                  "frame_3": self.third_frame}
        buttons = {"home": self.home_button,
                   "frame_2": self.frame_2_button,
                   "frame_3": self.frame_3_button}

        for frame_name, frame in frames.items():
            if frame_name == name:
                frame.grid(row=0, column=1, sticky="nsew")
                buttons[frame_name].configure(fg_color=("gray75", "gray25"))
            else:
                frame.grid_forget()
                buttons[frame_name].configure(fg_color="transparent")

    def home_button_event(self):
        """Event handler for the home button."""

        if hasattr(self, "scrollable_table_frame"):
            self.scrollable_table_frame.destroy()

        self.create_home_frame()
        self.select_frame_by_name("home")

    def delete_record_and_redirect(self, record_id):
        """
        Delete a record from the inventory table and redirect to the home.
        """

        if delete_record(record_id):
            self.home_button_event()

    def frame_2_button_event(self):
        """Event handler for the frame 2 button."""

        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        """Event handler for the frame 3 button."""

        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        """Event handler for changing the appearance mode."""

        ctk.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
