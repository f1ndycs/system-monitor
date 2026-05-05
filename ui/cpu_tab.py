"""Вкладка "Процессор"."""

import customtkinter as ctk


class CpuTab:
    def __init__(self, parent):
        self.parent = parent
        self.label = ctk.CTkLabel(parent, text="Загрузка процессора", font=ctk.CTkFont(size=18))
        self.label.pack(pady=20)

    def update(self):
        pass