"""
Модуль сбора метрик сети.
"""

import psutil


def format_speed(bytes_per_sec: float) -> str:
    """
    Преобразует байты/с в читаемый вид (B/s, KB/s, MB/s).
    """
    if bytes_per_sec < 1024:
        return f"{bytes_per_sec:.1f} B/s"
    elif bytes_per_sec < 1024 ** 2:
        return f"{bytes_per_sec / 1024:.1f} KB/s"
    else:
        return f"{bytes_per_sec / (1024 ** 2):.1f} MB/s"


def format_bytes(total_bytes: int) -> str:
    """
    Преобразует байты в читаемый вид (KB, MB, GB).
    """
    if total_bytes < 1024 ** 2:
        return f"{total_bytes / 1024:.1f} KB"
    elif total_bytes < 1024 ** 3:
        return f"{total_bytes / (1024 ** 2):.1f} MB"
    else:
        return f"{total_bytes / (1024 ** 3):.2f} GB"


def get_network_io() -> dict:
    """
    Возвращает общую статистику по всем сетевым интерфейсам (суммарно).
    """
    io = psutil.net_io_counters()
    return {
        'bytes_sent': io.bytes_sent,
        'bytes_recv': io.bytes_recv,
        'packets_sent': io.packets_sent,
        'packets_recv': io.packets_recv,
        'bytes_sent_formatted': format_bytes(io.bytes_sent),
        'bytes_recv_formatted': format_bytes(io.bytes_recv)
    }


def get_network_interfaces() -> dict:
    """
    Возвращает информацию по каждому сетевому интерфейсу.
    """
    interfaces = {}
    for name, addrs in psutil.net_if_addrs().items():
        interfaces[name] = []
        for addr in addrs:
            interfaces[name].append({
                'family': str(addr.family),
                'address': addr.address,
                'netmask': addr.netmask,
                'broadcast': addr.broadcast
            })
    return interfaces


def get_connection_count() -> dict:
    """
    Подсчитывает количество сетевых соединений по типам.
    """
    connections = psutil.net_connections()
    stats = {
        'total': len(connections),
        'tcp': 0,
        'udp': 0,
        'established': 0,
        'listen': 0
    }
    for conn in connections:
        if conn.type == 1:  # TCP
            stats['tcp'] += 1
            if conn.status == 'ESTABLISHED':
                stats['established'] += 1
            elif conn.status == 'LISTEN':
                stats['listen'] += 1
        elif conn.type == 2:  # UDP
            stats['udp'] += 1
    return stats


def get_network_stats() -> dict:
    """
    Возвращает полную сводку о сети.
    """
    return {
        'io': get_network_io(),
        'connections': get_connection_count()
    }


# Проверка при запуске файла напрямую
if __name__ == '__main__':
    stats = get_network_stats()
    io = stats['io']
    conn = stats['connections']

    print("=== СЕТЕВАЯ СТАТИСТИКА ===")
    print(f"Отправлено всего: {io['bytes_sent_formatted']}")
    print(f"Получено всего:   {io['bytes_recv_formatted']}")
    print(f"Пакетов отправлено: {io['packets_sent']}")
    print(f"Пакетов получено:   {io['packets_recv']}")

    print(f"\n=== СОЕДИНЕНИЯ ===")
    print(f"Всего:           {conn['total']}")
    print(f"TCP:              {conn['tcp']}")
    print(f"UDP:              {conn['udp']}")
    print(f"ESTABLISHED:      {conn['established']}")
    print(f"LISTEN:           {conn['listen']}")