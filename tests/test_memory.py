"""Тесты модуля сбора метрик памяти."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collector.memory import get_memory_stats


def test_get_memory_stats():
    """Проверяет структуру словаря с метриками памяти."""
    stats = get_memory_stats()
    assert 'virtual' in stats
    assert 'swap' in stats

    v = stats['virtual']
    assert 'total_gb' in v
    assert 'used_gb' in v
    assert 'percent' in v
    assert v['total_gb'] > 0
    assert 0 <= v['percent'] <= 100