"""Тесты модуля сбора метрик CPU."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collector.cpu import get_cpu_stats, get_cpu_percent, get_cpu_count


def test_get_cpu_percent():
    """Проверяет, что загрузка CPU — число от 0 до 100."""
    result = get_cpu_percent(interval=0.1)
    assert isinstance(result, float)
    assert 0.0 <= result <= 100.0


def test_get_cpu_count():
    """Проверяет, что количество ядер больше 0."""
    logical = get_cpu_count(logical=True)
    physical = get_cpu_count(logical=False)
    assert logical > 0
    assert physical > 0
    assert logical >= physical


def test_get_cpu_stats():
    """Проверяет структуру словаря с метриками CPU."""
    stats = get_cpu_stats()
    assert 'percent' in stats
    assert 'per_core' in stats
    assert 'cores_physical' in stats
    assert 'cores_logical' in stats
    assert 'frequency' in stats
    assert isinstance(stats['per_core'], list)
    assert len(stats['per_core']) == stats['cores_logical']