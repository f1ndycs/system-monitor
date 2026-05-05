"""
Вкладка "Память и сеть" — отображает использование RAM, Swap и сетевую активность.
"""

import customtkinter as ctk
from collector.memory import get_memory_stats
from collector.network import get_network_stats, format_speed


class MemoryTab:
    def __init__(self, parent):
        self.parent = parent

        # Заголовок
        memory_header = ctk.CTkLabel(
            parent,
            text="Оперативная память",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        memory_header.pack(pady=(15, 10))

        # Общая информация о памяти
        self.mem_info = ctk.CTkLabel(
            parent,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.mem_info.pack(pady=5)

        # Прогресс-бар памяти
        self.mem_bar = ctk.CTkProgressBar(parent, width=600)
        self.mem_bar.set(0)
        self.mem_bar.pack(pady=5)

        # Детали памяти в две колонки
        mem_details_frame = ctk.CTkFrame(parent)
        mem_details_frame.pack(fill="x", padx=20, pady=5)

        self.mem_used_label = ctk.CTkLabel(mem_details_frame, text="", font=ctk.CTkFont(size=13))
        self.mem_used_label.pack(side="left", padx=15)

        self.mem_free_label = ctk.CTkLabel(mem_details_frame, text="", font=ctk.CTkFont(size=13))
        self.mem_free_label.pack(side="left", padx=15)

        self.mem_cache_label = ctk.CTkLabel(mem_details_frame, text="", font=ctk.CTkFont(size=13))
        self.mem_cache_label.pack(side="left", padx=15)

        # ========== SWAP ==========
        swap_header = ctk.CTkLabel(
            parent,
            text="Подкачка (Swap)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        swap_header.pack(pady=(15, 5))

        self.swap_info = ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=14))
        self.swap_info.pack(pady=5)

        self.swap_bar = ctk.CTkProgressBar(parent, width=400)
        self.swap_bar.set(0)
        self.swap_bar.pack(pady=5)

        # ========== СЕТЬ ==========
        network_header = ctk.CTkLabel(
            parent,
            text="Сеть",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        network_header.pack(pady=(20, 10))

        # Статистика сети
        net_frame = ctk.CTkFrame(parent)
        net_frame.pack(fill="x", padx=20, pady=5)

        self.net_recv_label = ctk.CTkLabel(net_frame, text="", font=ctk.CTkFont(size=14))
        self.net_recv_label.pack(side="left", padx=15)

        self.net_sent_label = ctk.CTkLabel(net_frame, text="", font=ctk.CTkFont(size=14))
        self.net_sent_label.pack(side="left", padx=15)

        # Для подсчёта скорости нужно хранить предыдущие значения
        self._prev_recv = 0
        self._prev_sent = 0

    def update(self, data=None):
        """Обновляет данные памяти и сети."""
        try:
            if data:
                mem = data['memory']
                net = data['network']
            else:
                from collector.memory import get_memory_stats
                from collector.network import get_network_stats
                mem = get_memory_stats()
                net = get_network_stats()

            v = mem['virtual']
            s = mem['swap']

            self.mem_info.configure(
                text=f"Всего: {v['total_gb']} ГБ | Использовано: {v['used_gb']} ГБ ({v['percent']}%)"
            )
            self.mem_bar.set(v['percent'] / 100)

            self.mem_used_label.configure(text=f"Использовано: {v['used_gb']} ГБ")
            self.mem_free_label.configure(text=f"Свободно: {v['free_gb']} ГБ")
            self.mem_cache_label.configure(text=f"Кэш/буфер: {v['cached_gb']} ГБ")

            if s['total_gb'] > 0:
                self.swap_info.configure(
                    text=f"Всего: {s['total_gb']} ГБ | Использовано: {s['used_gb']} ГБ ({s['percent']}%)"
                )
                self.swap_bar.set(s['percent'] / 100)
            else:
                self.swap_info.configure(text="Swap недоступен")
                self.swap_bar.set(0)

            io = net['io']
            recv_speed = io['bytes_recv'] - self._prev_recv
            sent_speed = io['bytes_sent'] - self._prev_sent
            self._prev_recv = io['bytes_recv']
            self._prev_sent = io['bytes_sent']

            self.net_recv_label.configure(
                text=f"↓ Получение: {format_speed(recv_speed)}    (Всего: {io['bytes_recv_formatted']})"
            )
            self.net_sent_label.configure(
                text=f"↑ Отправка: {format_speed(sent_speed)}    (Всего: {io['bytes_sent_formatted']})"
            )

        except Exception as e:
            print(f"Ошибка обновления памяти/сети: {e}")