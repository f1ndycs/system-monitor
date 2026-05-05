"""
Модуль логирования.
Записывает события программы в файл system-monitor.log.
"""

import logging
import os
from datetime import datetime


def setup_logger(log_dir: str = None) -> logging.Logger:
    """
    Создаёт и настраивает логгер.
    """
    if log_dir is None:
        # Папка, где лежит logger.py → поднимаемся на уровень проекта
        log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    log_file = os.path.join(log_dir, "system-monitor.log")

    # Создаём логгер
    logger = logging.getLogger("SystemMonitor")
    logger.setLevel(logging.DEBUG)

    # Если уже есть обработчики — не добавляем повторно
    if logger.handlers:
        return logger

    # Формат сообщений
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Обработчик для файла
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# Глобальный логгер для всего проекта
logger = setup_logger()