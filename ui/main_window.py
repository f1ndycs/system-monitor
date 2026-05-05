"""
Главное окно приложения System Monitor.
"""

import customtkinter as ctk
import threading
from ui.cpu_tab import CpuTab
from ui.memory_tab import MemoryTab
from ui.disk_tab import DiskTab
from ui.processes_tab import ProcessesTab
from logger.logger import logger


class MainWindow:
    """Главное окно монитора системных ресурсов."""

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("System Monitor")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)

        # Данные для обмена между потоками
        self.cpu_data = None
        self.memory_data = None
        self.disk_data = None
        self.processes_data = None
        self._lock = threading.Lock()
        self._running = True

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

        self.tabview.add("Процессор")
        self.tabview.add("Память и сеть")
        self.tabview.add("Диски")
        self.tabview.add("Процессы")

        self.cpu_tab = CpuTab(self.tabview.tab("Процессор"))
        self.memory_tab = MemoryTab(self.tabview.tab("Память и сеть"))
        self.disk_tab = DiskTab(self.tabview.tab("Диски"))
        self.processes_tab = ProcessesTab(self.tabview.tab("Процессы"))

        # Кнопка выхода
        self.exit_button = ctk.CTkButton(
            self.root,
            text="Выход",
            command=self.on_exit,
            width=100
        )
        self.exit_button.pack(pady=(0, 10))

        # Запуск потоков сбора данных
        self._start_collector_threads()

        # Запуск обновления UI
        self.update_ui()

    def _start_collector_threads(self):
        """Запускает потоки для сбора метрик."""

        def collect_cpu():
            from collector.cpu import get_cpu_stats
            while self._running:
                try:
                    data = get_cpu_stats()
                    with self._lock:
                        self.cpu_data = data
                except Exception as e:
                    logger.error(f"Поток CPU: {e}")
                threading.Event().wait(1.0)

        def collect_memory():
            from collector.memory import get_memory_stats
            from collector.network import get_network_stats
            while self._running:
                try:
                    mem = get_memory_stats()
                    net = get_network_stats()
                    with self._lock:
                        self.memory_data = {'memory': mem, 'network': net}
                except Exception as e:
                    logger.error(f"Поток памяти: {e}")
                threading.Event().wait(1.0)

        def collect_disk():
            from collector.disk import get_disk_stats
            while self._running:
                try:
                    data = get_disk_stats()
                    with self._lock:
                        self.disk_data = data
                except Exception as e:
                    logger.error(f"Поток дисков: {e}")
                threading.Event().wait(1.0)

        def collect_processes():
            from collector.processes import get_process_stats
            while self._running:
                try:
                    data = get_process_stats()
                    with self._lock:
                        self.processes_data = data
                except Exception as e:
                    logger.error(f"Поток процессов: {e}")
                threading.Event().wait(1.0)

        threads = [
            threading.Thread(target=collect_cpu, daemon=True, name="Collector-CPU"),
            threading.Thread(target=collect_memory, daemon=True, name="Collector-Memory"),
            threading.Thread(target=collect_disk, daemon=True, name="Collector-Disk"),
            threading.Thread(target=collect_processes, daemon=True, name="Collector-Processes"),
        ]

        for t in threads:
            logger.info(f"Запуск потока: {t.name}")
            t.start()

    def update_ui(self):
        """Обновляет интерфейс данными из потоков."""
        if not self._running:
            return

        with self._lock:
            cpu_data = self.cpu_data
            memory_data = self.memory_data
            disk_data = self.disk_data
            processes_data = self.processes_data

        if cpu_data:
            self.cpu_tab.update(cpu_data)
        if memory_data:
            self.memory_tab.update(memory_data)
        if disk_data:
            self.disk_tab.update(disk_data)
        if processes_data:
            self.processes_tab.update(processes_data)

        self.root.after(1000, self.update_ui)

    def on_exit(self):
        """Корректное завершение всех потоков."""
        logger.info("Завершение работы...")
        self._running = False
        self.root.destroy()

    def run(self):
        self.root.mainloop()