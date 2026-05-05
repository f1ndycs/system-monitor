"""
System Monitor — утилита мониторинга системных ресурсов в Linux.
"""

from ui.main_window import MainWindow


def main():
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()