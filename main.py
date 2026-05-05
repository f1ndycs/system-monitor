"""
System Monitor — утилита мониторинга системных ресурсов в Linux.
"""

from ui.main_window import MainWindow
from logger.logger import logger


def main():
    logger.info("Запуск System Monitor")
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        logger.exception("Критическая ошибка приложения")
    finally:
        logger.info("Завершение System Monitor")


if __name__ == "__main__":
    main()