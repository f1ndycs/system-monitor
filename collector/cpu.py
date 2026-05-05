"""
Модуль сбора метрик процессора.
Использует библиотеку psutil для получения данных из /proc/stat.
"""

import psutil


def get_cpu_percent(interval: float = 0.1) -> float:
    """
    Возвращает общую загрузку CPU в процентах.
    """
    return psutil.cpu_percent(interval=interval)


def get_cpu_percent_per_core(interval: float = 0.1) -> list[float]:
    """
    Возвращает загрузку каждого ядра CPU в процентах.
    """
    return psutil.cpu_percent(interval=interval, percpu=True)


def get_cpu_count(logical: bool = True) -> int:
    """
    Возвращает количество ядер CPU.

    Args:
        logical: True — логические ядра (с HyperThreading),
                 False — только физические

    Returns:
        int: количество ядер
    """
    return psutil.cpu_count(logical=logical)


def get_cpu_frequency() -> dict:
    """
    Возвращает текущую, минимальную и максимальную частоту CPU.
    """
    freq = psutil.cpu_freq()
    return {
        'current': round(freq.current, 1) if freq.current else 0,
        'min': round(freq.min, 1) if freq.min else 0,
        'max': round(freq.max, 1) if freq.max else 0
    }


def get_cpu_stats() -> dict:
    """
    Возвращает полную сводку о процессоре.
    """
    return {
        'percent': get_cpu_percent(),
        'per_core': get_cpu_percent_per_core(),
        'cores_physical': get_cpu_count(logical=False),
        'cores_logical': get_cpu_count(logical=True),
        'frequency': get_cpu_frequency()
    }


# Проверка при запуске файла напрямую
if __name__ == '__main__':
    stats = get_cpu_stats()
    print(f"Загрузка CPU: {stats['percent']}%")
    print(f"По ядрам: {stats['per_core']}")
    print(f"Ядер физических: {stats['cores_physical']}")
    print(f"Ядер логических: {stats['cores_logical']}")
    print(f"Частота: {stats['frequency']}")