"""Тесты модуля сбора метрик сети."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collector.network import get_network_stats, format_speed, format_bytes


def test_format_speed():
    """Проверяет форматирование скорости."""
    assert 'B/s' in format_speed(500)
    assert 'KB/s' in format_speed(1500)
    assert 'MB/s' in format_speed(2000000)


def test_format_bytes():
    """Проверяет форматирование байт."""
    assert 'KB' in format_bytes(5000)
    assert 'MB' in format_bytes(5000000)
    assert 'GB' in format_bytes(5000000000)


def test_get_network_stats():
    """Проверяет структуру словаря с метриками сети."""
    stats = get_network_stats()
    assert 'io' in stats
    assert 'connections' in stats
    assert 'bytes_sent' in stats['io']
    assert 'bytes_recv' in stats['io']