"""
Модуль сбора метрик дисков (разделы и ввод/вывод).
"""

import psutil


def get_disk_partitions() -> list[dict]:
    """
    Возвращает список разделов диска с информацией о занятом месте.
    """
    partitions = []
    for part in psutil.disk_partitions():
        # Пропускаем виртуальные и системные разделы
        if 'loop' in part.device or 'snap' in part.mountpoint:
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                'device': part.device,
                'mountpoint': part.mountpoint,
                'filesystem': part.fstype,
                'total_gb': round(usage.total / (1024 ** 3), 1),
                'used_gb': round(usage.used / (1024 ** 3), 1),
                'free_gb': round(usage.free / (1024 ** 3), 1),
                'percent': usage.percent
            })
        except PermissionError:
            continue
    return partitions


def get_disk_io() -> dict:
    """
    Возвращает статистику ввода/вывода по всем дискам.
    """
    io = psutil.disk_io_counters()
    return {
        'read_bytes_total_gb': round(io.read_bytes / (1024 ** 3), 2),
        'write_bytes_total_gb': round(io.write_bytes / (1024 ** 3), 2),
        'read_count': io.read_count,
        'write_count': io.write_count
    }


def get_disk_stats() -> dict:
    """
    Возвращает полную сводку о дисках.
    """
    return {
        'partitions': get_disk_partitions(),
        'io': get_disk_io()
    }


# Проверка при запуске файла напрямую
if __name__ == '__main__':
    stats = get_disk_stats()

    print("=== РАЗДЕЛЫ ДИСКА ===")
    for part in stats['partitions']:
        print(f"\nУстройство:  {part['device']}")
        print(f"Точка монтирования: {part['mountpoint']}")
        print(f"Файловая система:   {part['filesystem']}")
        print(f"Всего:    {part['total_gb']} ГБ")
        print(f"Занято:   {part['used_gb']} ГБ ({part['percent']}%)")
        print(f"Свободно: {part['free_gb']} ГБ")

    print(f"\n=== ВВОД/ВЫВОД ===")
    io = stats['io']
    print(f"Прочитано всего:  {io['read_bytes_total_gb']} ГБ")
    print(f"Записано всего:   {io['write_bytes_total_gb']} ГБ")
    print(f"Операций чтения:  {io['read_count']}")
    print(f"Операций записи:  {io['write_count']}")