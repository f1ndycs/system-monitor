FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Запуск в консольном режиме (без GUI)
CMD ["python", "-c", "from collector.cpu import get_cpu_stats; from collector.memory import get_memory_stats; from collector.disk import get_disk_stats; from collector.network import get_network_stats; from collector.processes import get_process_stats; import json; print(json.dumps({'cpu': get_cpu_stats(), 'memory': get_memory_stats(), 'disk': get_disk_stats(), 'network': get_network_stats(), 'processes': get_process_stats()}, indent=2, default=str))"]