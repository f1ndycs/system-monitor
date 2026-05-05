"""
Главное окно приложения System Monitor.
Использует CustomTkinter для современного интерфейса.
"""

import customtkinter as ctk
from ui.cpu_tab import CpuTab
from ui.memory_tab import MemoryTab
from ui.disk_tab import DiskTab
from ui.processes_tab import ProcessesTab


class MainWindow:
    """Главное окно монитора системных ресурсов."""

    def __init__(self):
        # Настройка темы
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Создание окна
        self.root = ctk.CTk()
        self.root.title("System Monitor")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)

        # Заголовок
        self.title_label = ctk.CTkLabel(
            self.root,
            text="System Monitor",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(15, 5))

        # Вкладки
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Добавляем вкладки
        self.tabview.add("Процессор")
        self.tabview.add("Память и сеть")
        self.tabview.add("Диски")
        self.tabview.add("Процессы")

        # Создаём содержимое вкладок (пока заглушки)
        self.cpu_tab = CpuTab(self.tabview.tab("Процессор"))
        self.memory_tab = MemoryTab(self.tabview.tab("Память и сеть"))
        self.disk_tab = DiskTab(self.tabview.tab("Диски"))
        self.processes_tab = ProcessesTab(self.tabview.tab("Процессы"))

        # Кнопка выхода внизу
        self.exit_button = ctk.CTkButton(
            self.root,
            text="Выход",
            command=self.root.destroy,
            width=100
        )
        self.exit_button.pack(pady=(0, 10))

        # Запуск обновления каждую секунду
        self.update_all()

    def update_all(self):
        """Обновляет данные на всех вкладках."""
        try:
            self.cpu_tab.update()
        except Exception as e:
            from logger.logger import logger
            logger.error(f"Ошибка обновления CPU: {e}")

        try:
            self.memory_tab.update()
        except Exception as e:
            from logger.logger import logger
            logger.error(f"Ошибка обновления памяти: {e}")

        try:
            self.disk_tab.update()
        except Exception as e:
            from logger.logger import logger
            logger.error(f"Ошибка обновления дисков: {e}")

        try:
            self.processes_tab.update()
        except Exception as e:
            from logger.logger import logger
            logger.error(f"Ошибка обновления процессов: {e}")

        self.root.after(1000, self.update_all)

    def run(self):
        """Запускает главный цикл приложения."""
        self.root.mainloop()