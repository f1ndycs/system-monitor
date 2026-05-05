"""
Модуль сбора метрик оперативной памяти и swap.
"""

import psutil


def get_virtual_memory() -> dict:
    """
    Возвращает информацию об оперативной памяти.
    """
    mem = psutil.virtual_memory()
    return {
        'total_gb': round(mem.total / (1024 ** 3), 1),
        'available_gb': round(mem.available / (1024 ** 3), 1),
        'used_gb': round(mem.used / (1024 ** 3), 1),
        'free_gb': round(mem.free / (1024 ** 3), 1),
        'percent': mem.percent,
        'cached_gb': round(getattr(mem, 'cached', 0) / (1024 ** 3), 1),
        'buffers_gb': round(getattr(mem, 'buffers', 0) / (1024 ** 3), 1)
    }


def get_swap_memory() -> dict:
    """
    Возвращает информацию о swap (подкачке).
    """
    swap = psutil.swap_memory()
    return {
        'total_gb': round(swap.total / (1024 ** 3), 1),
        'used_gb': round(swap.used / (1024 ** 3), 1),
        'free_gb': round(swap.free / (1024 ** 3), 1),
        'percent': swap.percent
    }


def get_memory_stats() -> dict:
    """
    Возвращает полную сводку о памяти.
    """
    return {
        'virtual': get_virtual_memory(),
        'swap': get_swap_memory()
    }


# Проверка при запуске файла напрямую
if __name__ == '__main__':
    mem = get_memory_stats()
    v = mem['virtual']
    s = mem['swap']

    print(f"=== ОПЕРАТИВНАЯ ПАМЯТЬ ===")
    print(f"Всего:      {v['total_gb']} ГБ")
    print(f"Использовано: {v['used_gb']} ГБ ({v['percent']}%)")
    print(f"Свободно:   {v['free_gb']} ГБ")
    print(f"Доступно:   {v['available_gb']} ГБ")
    print(f"Кэш:        {v['cached_gb']} ГБ")
    print(f"Буферы:     {v['buffers_gb']} ГБ")

    print(f"\n=== ПОДКАЧКА (SWAP) ===")
    print(f"Всего:      {s['total_gb']} ГБ")
    print(f"Использовано: {s['used_gb']} ГБ ({s['percent']}%)")
    print(f"Свободно:   {s['free_gb']} ГБ")