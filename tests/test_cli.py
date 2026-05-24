"""Интеграционные тесты CLI."""

import os
import subprocess
import sys

# Принудительно UTF-8 для всех subprocess-тестов
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def _run_cli(*args):
    """Хелпер для запуска CLI в subprocess."""
    return subprocess.run(
        [sys.executable, "-m", "mortgage_calc.cli", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=ENV,
    )


def test_cli_help():
    """Проверка --help."""
    result = _run_cli("--help")
    assert result.returncode == 0
    assert "Сумма кредита" in result.stdout or "amount" in result.stdout


def test_cli_basic():
    """Базовый запуск CLI."""
    result = _run_cli("--amount", "1000000", "--rate", "12", "--years", "1")
    assert result.returncode == 0
    assert "Ежемесячный платёж" in result.stdout


def test_cli_json():
    """Вывод в JSON."""
    result = _run_cli("--amount", "100000", "--rate", "0", "--years", "1", "--format", "json")
    assert result.returncode == 0
    assert '"monthly_payment": 8333.33' in result.stdout


def test_cli_error():
    """Обработка ошибки."""
    result = _run_cli("--amount", "-1000", "--rate", "10", "--years", "5")
    assert result.returncode == 1
    assert "Ошибка" in result.stderr