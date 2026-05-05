"""Вкладка "Диски"."""

import customtkinter as ctk


class DiskTab:
    def __init__(self, parent):
        self.parent = parent
        self.label = ctk.CTkLabel(parent, text="Диски", font=ctk.CTkFont(size=18))
        self.label.pack(pady=20)

    def update(self):
        pass