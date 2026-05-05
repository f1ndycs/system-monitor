"""Вкладка "Процессы"."""

import customtkinter as ctk


class ProcessesTab:
    def __init__(self, parent):
        self.parent = parent
        self.label = ctk.CTkLabel(parent, text="Процессы", font=ctk.CTkFont(size=18))
        self.label.pack(pady=20)

    def update(self):
        pass