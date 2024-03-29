# src/screens/initial_screen.py
import tkinter as tk
from customtkinter import CustomTkinter as ctk


class InitialScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Initial Screen")

        self.label = ctk.CTkLabel(
            root,
            text="Welcome to Initial Screen",
            font=("Helvetica", 24),
            bg=ctk.colors["primary"],
            fg=ctk.colors["light"]
        )
        self.label.pack(padx=20, pady=20)


def main():
    root = tk.Tk()
    app = InitialScreen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
