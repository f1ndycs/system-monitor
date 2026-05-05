#!/bin/bash
# Скрипт запуска System Monitor
# Даёт полный доступ к /proc хоста (в отличие от Docker)

echo "Запуск System Monitor..."
cd "$(dirname "$0")"
python main.py