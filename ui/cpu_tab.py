"""
Вкладка "Процессор" — отображает загрузку CPU общую и по ядрам.
"""

import customtkinter as ctk
from collector.cpu import get_cpu_stats


class CpuTab:
    def __init__(self, parent):
        self.parent = parent

        # Заголовок
        header = ctk.CTkLabel(
            parent,
            text="Мониторинг процессора",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header.pack(pady=(15, 10))

        # Общая информация
        self.info_frame = ctk.CTkFrame(parent)
        self.info_frame.pack(fill="x", padx=20, pady=5)

        self.cores_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.cores_label.pack(side="left", padx=10)

        self.freq_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.freq_label.pack(side="right", padx=10)

        # Общая загрузка CPU
        self.total_label = ctk.CTkLabel(
            parent,
            text="Общая загрузка: --%",
            font=ctk.CTkFont(size=16)
        )
        self.total_label.pack(pady=5)

        self.total_bar = ctk.CTkProgressBar(parent, width=600)
        self.total_bar.set(0)
        self.total_bar.pack(pady=5)

        # Загрузка по ядрам
        self.cores_label_header = ctk.CTkLabel(
            parent,
            text="Загрузка по ядрам:",
            font=ctk.CTkFont(size=14)
        )
        self.cores_label_header.pack(pady=(15, 5))

        self.cores_frame = ctk.CTkScrollableFrame(parent, height=250)
        self.cores_frame.pack(fill="x", padx=20, pady=(0, 10), expand=False)

        # Список баров для ядер (создадим при первом обновлении)
        self.core_bars = []
        self.core_labels = []

    def update(self):
        """Обновляет данные процессора."""
        try:
            stats = get_cpu_stats()

            self.cores_label.configure(
                text=f"Ядер: {stats['cores_physical']} физ. / {stats['cores_logical']} лог."
            )

            freq = stats['frequency']
            if freq['min'] > 0 and freq['max'] > 0:
                freq_text = f"Частота: {freq['current']:.0f} МГц (мин: {freq['min']:.0f}, макс: {freq['max']:.0f})"
            else:
                freq_text = f"Частота: {freq['current']:.0f} МГц"

            self.freq_label.configure(text=freq_text)

            total_pct = stats['percent']
            self.total_label.configure(text=f"Общая загрузка: {total_pct:.1f}%")
            self.total_bar.set(total_pct / 100)

            per_core = stats['per_core']

            if not self.core_bars:
                for i in range(len(per_core)):
                    frame = ctk.CTkFrame(self.cores_frame)
                    frame.pack(fill="x", pady=2)

                    label = ctk.CTkLabel(frame, text=f"Ядро {i + 1}:", width=80)
                    label.pack(side="left", padx=5)

                    bar = ctk.CTkProgressBar(frame)
                    bar.pack(side="left", fill="x", expand=True, padx=5)

                    pct_label = ctk.CTkLabel(frame, text="", width=50)
                    pct_label.pack(side="right", padx=5)

                    self.core_bars.append(bar)
                    self.core_labels.append(pct_label)

            for i, pct in enumerate(per_core):
                if i < len(self.core_bars):
                    self.core_bars[i].set(pct / 100)
                    self.core_labels[i].configure(text=f"{pct:.1f}%")

        except Exception as e:
            print(f"Ошибка обновления CPU: {e}")