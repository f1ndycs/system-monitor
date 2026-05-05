"""
Вкладка "Диски" — отображает информацию о разделах и вводе/выводе.
"""

import customtkinter as ctk
from collector.disk import get_disk_stats


class DiskTab:
    def __init__(self, parent):
        self.parent = parent

        # Заголовок
        header = ctk.CTkLabel(
            parent,
            text="Дисковое пространство",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header.pack(pady=(15, 10))

        # Прокручиваемая область для разделов
        self.partitions_frame = ctk.CTkScrollableFrame(parent, height=300)
        self.partitions_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Список фреймов разделов
        self.partition_frames = []

        # Статистика ввода/вывода
        io_header = ctk.CTkLabel(
            parent,
            text="Ввод/Вывод",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        io_header.pack(pady=(15, 5))

        io_frame = ctk.CTkFrame(parent)
        io_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.io_read_label = ctk.CTkLabel(io_frame, text="", font=ctk.CTkFont(size=14))
        self.io_read_label.pack(side="left", padx=15, pady=5)

        self.io_write_label = ctk.CTkLabel(io_frame, text="", font=ctk.CTkFont(size=14))
        self.io_write_label.pack(side="left", padx=15, pady=5)

    def update(self):
        """Обновляет данные о дисках."""
        try:
            stats = get_disk_stats()
            partitions = stats['partitions']

            # Создаём или обновляем блоки для каждого раздела
            for i, part in enumerate(partitions):
                if i >= len(self.partition_frames):
                    # Создаём новый фрейм для раздела
                    part_frame = ctk.CTkFrame(self.partitions_frame)
                    part_frame.pack(fill="x", pady=5)

                    # Заголовок раздела
                    title = ctk.CTkLabel(
                        part_frame,
                        text="",
                        font=ctk.CTkFont(size=15, weight="bold")
                    )
                    title.pack(anchor="w", padx=10, pady=(5, 0))

                    # Прогресс-бар
                    bar = ctk.CTkProgressBar(part_frame)
                    bar.pack(fill="x", padx=10, pady=5)

                    # Детали
                    details = ctk.CTkLabel(
                        part_frame,
                        text="",
                        font=ctk.CTkFont(size=13)
                    )
                    details.pack(anchor="w", padx=10, pady=(0, 5))

                    self.partition_frames.append({
                        'frame': part_frame,
                        'title': title,
                        'bar': bar,
                        'details': details
                    })

                # Обновляем данные
                if i < len(self.partition_frames):
                    widgets = self.partition_frames[i]
                    widgets['title'].configure(
                        text=f"{part['device']} — {part['mountpoint']} ({part['filesystem']})"
                    )
                    widgets['bar'].set(part['percent'] / 100)
                    widgets['details'].configure(
                        text=f"Занято: {part['used_gb']} ГБ / {part['total_gb']} ГБ ({part['percent']}%)  |  Свободно: {part['free_gb']} ГБ"
                    )

            # Скрываем лишние фреймы, если разделов стало меньше
            for i in range(len(partitions), len(self.partition_frames)):
                self.partition_frames[i]['frame'].pack_forget()

            # Статистика ввода/вывода
            io = stats['io']
            self.io_read_label.configure(
                text=f"Прочитано всего: {io['read_bytes_total_gb']} ГБ (операций: {io['read_count']})"
            )
            self.io_write_label.configure(
                text=f"Записано всего: {io['write_bytes_total_gb']} ГБ (операций: {io['write_count']})"
            )

        except Exception as e:
            print(f"Ошибка обновления дисков: {e}")