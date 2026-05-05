"""Тесты модуля сбора метрик дисков."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collector.disk import get_disk_stats


def test_get_disk_stats():
    """Проверяет структуру словаря с метриками дисков."""
    stats = get_disk_stats()
    assert 'partitions' in stats
    assert 'io' in stats
    assert isinstance(stats['partitions'], list)

    if stats['partitions']:
        part = stats['partitions'][0]
        assert 'device' in part
        assert 'mountpoint' in part
        assert 'total_gb' in part
        assert 'percent' in part