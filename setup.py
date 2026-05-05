"""
Установочный пакет System Monitor.
"""

from setuptools import setup, find_packages

setup(
    name="system-monitor",
    version="1.0.0",
    description="Утилита мониторинга системных ресурсов в Linux",
    author="Паус Максим Борисович",
    packages=find_packages(),
    py_modules=['main'],
    install_requires=[
        "psutil",
        "matplotlib",
        "customtkinter",
    ],
    entry_points={
        "console_scripts": [
            "system-monitor=main:main",
        ],
    },
    python_requires=">=3.10",
)