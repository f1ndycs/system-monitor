"""
Вкладка "Процессор" — графики загрузки CPU (общий и по ядрам).
"""

import customtkinter as ctk
from collector.cpu import get_cpu_stats
from collections import deque

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CpuTab:
    def __init__(self, parent):
        self.parent = parent

        self.history_size = 60
        self.history_total = deque([0] * self.history_size, maxlen=self.history_size)
        self.history_cores = {}
        self.core_graphs = {}
        self._first_update = True

        # Заголовок
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 0))

        header = ctk.CTkLabel(
            header_frame,
            text="Мониторинг процессора",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header.pack(side="left")

        self.total_label = ctk.CTkLabel(
            header_frame,
            text="0%",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4fc3f7"
        )
        self.total_label.pack(side="right")

        # Инфо: ядра и частота
        self.info_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.info_frame.pack(fill="x", padx=15, pady=2)

        self.cores_label = ctk.CTkLabel(self.info_frame, text="", font=ctk.CTkFont(size=13))
        self.cores_label.pack(side="left")

        self.freq_label = ctk.CTkLabel(self.info_frame, text="", font=ctk.CTkFont(size=13))
        self.freq_label.pack(side="right")

        # Основной контейнер для всех графиков
        self.graphs_frame = ctk.CTkScrollableFrame(parent)
        self.graphs_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Сначала создаём контейнер для общего графика
        self.total_graph_container = ctk.CTkFrame(self.graphs_frame, fg_color="transparent")
        self.total_graph_container.pack(fill="x", pady=(0, 10))

        self.fig_total = Figure(figsize=(10, 1.8), dpi=100, facecolor='#2b2b2b')
        self.ax_total = self.fig_total.add_subplot(111)
        self.ax_total.set_facecolor('#1e1e1e')
        self.ax_total.set_ylim(0, 105)
        self.ax_total.set_xlim(0, self.history_size - 1)
        self.ax_total.tick_params(colors='#888888', labelsize=8, pad=2)
        self.ax_total.spines['bottom'].set_color('#444444')
        self.ax_total.spines['left'].set_color('#444444')
        self.ax_total.spines['top'].set_visible(False)
        self.ax_total.spines['right'].set_visible(False)
        self.ax_total.set_xticks([0, 15, 30, 45, 59])
        self.ax_total.set_xticklabels(['60с', '45с', '30с', '15с', '0с'])
        self.ax_total.set_yticks([0, 25, 50, 75, 100])
        self.line_total, = self.ax_total.plot([], [], color='#4fc3f7', linewidth=1.8, alpha=0.9)

        self.canvas_total = FigureCanvasTkAgg(self.fig_total, self.total_graph_container)
        self.canvas_total.get_tk_widget().pack(fill="x", expand=True)

        # Разделитель
        separator = ctk.CTkFrame(self.graphs_frame, height=1, fg_color="#444444")
        separator.pack(fill="x", pady=5)

        # Контейнер для графиков ядер
        self.cores_container = ctk.CTkFrame(self.graphs_frame, fg_color="transparent")
        self.cores_container.pack(fill="x")

    def update(self, data=None):
        try:
            if data:
                stats = data
            else:
                from collector.cpu import get_cpu_stats
                stats = get_cpu_stats()

            # Информация
            self.cores_label.configure(
                text=f"Ядер: {stats['cores_physical']} физ. / {stats['cores_logical']} лог."
            )
            freq = stats['frequency']
            if freq['min'] > 0 and freq['max'] > 0:
                freq_text = f"Частота: {freq['current']:.0f} МГц"
            else:
                freq_text = f"Частота: {freq['current']:.0f} МГц"
            self.freq_label.configure(text=freq_text)

            # Общая загрузка
            total_pct = stats['percent']
            self.total_label.configure(text=f"{total_pct:.1f}%")
            self.history_total.append(total_pct)

            # Обновляем общий график
            x = list(range(len(self.history_total)))
            self.line_total.set_data(x, list(self.history_total))
            self.canvas_total.draw_idle()

            # Ядра
            per_core = stats['per_core']

            if self._first_update:
                for i in range(len(per_core)):
                    self.history_cores[i] = deque([0] * self.history_size, maxlen=self.history_size)
                self._first_update = False

            for i, pct in enumerate(per_core):
                if i not in self.history_cores:
                    self.history_cores[i] = deque([0] * self.history_size, maxlen=self.history_size)
                self.history_cores[i].append(pct)

            # Создаём/обновляем графики ядер
            colors = ['#81c784', '#64b5f6', '#ffb74d', '#e57373', '#ba68c8', '#4dd0e1', '#f06292', '#aed581']

            for i in range(len(per_core)):
                if i not in self.core_graphs:
                    container = ctk.CTkFrame(self.cores_container, fg_color="transparent")
                    container.pack(fill="x", pady=1)

                    fig = Figure(figsize=(10, 1.0), dpi=100, facecolor='#2b2b2b')
                    ax = fig.add_subplot(111)
                    ax.set_facecolor('#1e1e1e')
                    ax.set_ylim(0, 105)
                    ax.set_xlim(0, self.history_size - 1)
                    ax.tick_params(colors='#888888', labelsize=7, pad=1)
                    ax.spines['bottom'].set_color('#444444')
                    ax.spines['left'].set_color('#444444')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.set_xticks([])
                    ax.set_yticks([0, 50, 100])

                    color = colors[i % len(colors)]
                    line, = ax.plot([], [], color=color, linewidth=1.3, alpha=0.85)

                    # Подпись ядра и процент слева
                    ax.set_ylabel(f'Я{i+1}', color=color, fontsize=8, rotation=0, labelpad=15)
                    ax.yaxis.set_label_coords(-0.06, 0.5)

                    canvas = FigureCanvasTkAgg(fig, container)
                    canvas.get_tk_widget().pack(fill="x", expand=True)

                    self.core_graphs[i] = {
                        'container': container,
                        'fig': fig,
                        'ax': ax,
                        'canvas': canvas,
                        'line': line
                    }

                g = self.core_graphs[i]
                x = list(range(len(self.history_cores[i])))
                g['line'].set_data(x, list(self.history_cores[i]))

                # Обновляем процент в подписи
                current_pct = self.history_cores[i][-1]
                g['ax'].set_ylabel(f'Я{i+1} {current_pct:.0f}%',
                                   color=colors[i % len(colors)],
                                   fontsize=8, rotation=0, labelpad=25)
                g['ax'].yaxis.set_label_coords(-0.08, 0.5)

                g['canvas'].draw_idle()

            # Удаляем лишние графики
            to_remove = [i for i in self.core_graphs if i >= len(per_core)]
            for i in to_remove:
                self.core_graphs[i]['container'].destroy()
                del self.core_graphs[i]

        except Exception as e:
            print(f"Ошибка обновления CPU: {e}")