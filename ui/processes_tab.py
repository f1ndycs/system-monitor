"""
Вкладка "Процессы" — отображает топ процессов по CPU и памяти.
"""

import customtkinter as ctk
from collector.processes import get_process_stats


class ProcessesTab:
    def __init__(self, parent):
        self.parent = parent

        # Заголовок и общее количество
        top_frame = ctk.CTkFrame(parent)
        top_frame.pack(fill="x", padx=20, pady=(15, 5))

        header = ctk.CTkLabel(
            top_frame,
            text="Процессы",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header.pack(side="left", padx=10)

        self.total_label = ctk.CTkLabel(
            top_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.total_label.pack(side="right", padx=10)

        # Две таблицы рядом: CPU и память
        tables_frame = ctk.CTkFrame(parent)
        tables_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Левая колонка — топ по CPU
        cpu_frame = ctk.CTkFrame(tables_frame)
        cpu_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        cpu_header = ctk.CTkLabel(
            cpu_frame,
            text="Топ по CPU",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cpu_header.pack(pady=5)

        # Заголовки столбцов
        cpu_cols = ctk.CTkFrame(cpu_frame)
        cpu_cols.pack(fill="x", padx=5)

        ctk.CTkLabel(cpu_cols, text="PID", width=60, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        ctk.CTkLabel(cpu_cols, text="CPU%", width=60, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        ctk.CTkLabel(cpu_cols, text="Процесс", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", fill="x", expand=True)

        self.cpu_list_frame = ctk.CTkScrollableFrame(cpu_frame, height=350)
        self.cpu_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.cpu_rows = []

        # Правая колонка — топ по памяти
        mem_frame = ctk.CTkFrame(tables_frame)
        mem_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        mem_header = ctk.CTkLabel(
            mem_frame,
            text="Топ по памяти",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        mem_header.pack(pady=5)

        mem_cols = ctk.CTkFrame(mem_frame)
        mem_cols.pack(fill="x", padx=5)

        ctk.CTkLabel(mem_cols, text="PID", width=60, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        ctk.CTkLabel(mem_cols, text="MEM%", width=60, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        ctk.CTkLabel(mem_cols, text="Процесс", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", fill="x", expand=True)

        self.mem_list_frame = ctk.CTkScrollableFrame(mem_frame, height=350)
        self.mem_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.mem_rows = []

    def update(self, data=None):
        """Обновляет список процессов."""
        try:
            if data:
                stats = data
            else:
                from collector.processes import get_process_stats
                stats = get_process_stats()

            # Общее количество
            self.total_label.configure(text=f"Всего процессов: {stats['total_count']}")

            # Обновляем топ CPU
            self._update_rows(
                self.cpu_list_frame,
                self.cpu_rows,
                stats['top_cpu'],
                value_key='cpu_percent',
                suffix='%'
            )

            # Обновляем топ памяти
            self._update_rows(
                self.mem_list_frame,
                self.mem_rows,
                stats['top_memory'],
                value_key='memory_percent',
                suffix='%'
            )

        except Exception as e:
            print(f"Ошибка обновления процессов: {e}")

    def _update_rows(self, parent_frame, row_widgets, process_list, value_key, suffix):
        """Обновляет строки в списке процессов."""
        # Создаём недостающие строки
        while len(row_widgets) < len(process_list):
            row_frame = ctk.CTkFrame(parent_frame)
            row_frame.pack(fill="x", pady=1)

            pid_label = ctk.CTkLabel(row_frame, text="", width=60, font=ctk.CTkFont(size=12))
            pid_label.pack(side="left")

            value_label = ctk.CTkLabel(row_frame, text="", width=60, font=ctk.CTkFont(size=12))
            value_label.pack(side="left")

            name_label = ctk.CTkLabel(row_frame, text="", font=ctk.CTkFont(size=12), anchor="w")
            name_label.pack(side="left", fill="x", expand=True)

            row_widgets.append({
                'frame': row_frame,
                'pid': pid_label,
                'value': value_label,
                'name': name_label
            })

        # Обновляем данные
        for i, proc in enumerate(process_list):
            if i < len(row_widgets):
                w = row_widgets[i]
                w['pid'].configure(text=str(proc['pid']))
                w['value'].configure(text=f"{proc[value_key]}{suffix}")
                name = proc['name'] or '?'
                # Обрезаем длинные имена
                if len(name) > 30:
                    name = name[:27] + '...'
                w['name'].configure(text=name)
                w['frame'].pack(fill="x", pady=1)

        # Скрываем лишние строки
        for i in range(len(process_list), len(row_widgets)):
            row_widgets[i]['frame'].pack_forget()