"""
Модуль сбора информации о запущенных процессах.
"""

import psutil
import time


def get_process_list(sort_by: str = 'cpu', limit: int = 20) -> list[dict]:
    """
    Возвращает список процессов, отсортированный по заданному критерию.
    Для точного измерения CPU делает два замера с паузой.
    """
    # Первый замер — холостой (просто дёргаем cpu_percent у всех)
    for proc in psutil.process_iter(['pid']):
        try:
            proc.cpu_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    time.sleep(0.5)

    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            cpu = proc.cpu_percent() or 0
            mem = proc.memory_percent() or 0

            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'cpu_percent': round(cpu, 1),
                'memory_percent': round(mem, 1),
                'status': proc.info['status']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if sort_by == 'cpu':
        processes.sort(key=lambda p: p['cpu_percent'], reverse=True)
    elif sort_by == 'memory':
        processes.sort(key=lambda p: p['memory_percent'], reverse=True)
    elif sort_by == 'pid':
        processes.sort(key=lambda p: p['pid'])
    elif sort_by == 'name':
        processes.sort(key=lambda p: (p['name'] or '').lower())

    return processes[:limit]


def get_total_process_count() -> int:
    """
    Возвращает общее количество запущенных процессов.
    """
    return len(psutil.pids())


def get_process_stats() -> dict:
    """
    Возвращает полную сводку о процессах.
    """
    return {
        'total_count': get_total_process_count(),
        'top_cpu': get_process_list(sort_by='cpu', limit=10),
        'top_memory': get_process_list(sort_by='memory', limit=10)
    }


# Проверка при запуске файла напрямую
if __name__ == '__main__':
    stats = get_process_stats()

    print(f"=== ВСЕГО ПРОЦЕССОВ: {stats['total_count']} ===\n")

    print("=== ТОП-10 ПО CPU ===")
    print(f"{'PID':<8} {'CPU%':<8} {'MEM%':<8} {'Имя':<30}")
    print("-" * 60)
    for proc in stats['top_cpu']:
        print(f"{proc['pid']:<8} {proc['cpu_percent']:<8} {proc['memory_percent']:<8} {proc['name'] or '?':<30}")

    print(f"\n=== ТОП-10 ПО ПАМЯТИ ===")
    print(f"{'PID':<8} {'CPU%':<8} {'MEM%':<8} {'Имя':<30}")
    print("-" * 60)
    for proc in stats['top_memory']:
        print(f"{proc['pid']:<8} {proc['cpu_percent']:<8} {proc['memory_percent']:<8} {proc['name'] or '?':<30}")