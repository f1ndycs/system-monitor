"""Вкладка "Память и сеть"."""

import customtkinter as ctk


class MemoryTab:
    def __init__(self, parent):
        self.parent = parent
        self.label = ctk.CTkLabel(parent, text="Память и сеть", font=ctk.CTkFont(size=18))
        self.label.pack(pady=20)

    def update(self):
        pass