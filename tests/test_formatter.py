"""Тесты форматирования."""

from mortgage_calc.calculator import calculate
from mortgage_calc.formatter import format_currency, format_schedule_table, format_summary


def test_format_currency():
    """Форматирование валюты."""
    assert format_currency(1000) == "1 000.00 ₽"
    assert format_currency(1234567.89) == "1 234 567.89 ₽"


def test_format_summary():
    """Форматирование сводки."""
    result = calculate(amount=1_000_000, annual_rate=12.0, years=1)
    summary = format_summary(result)
    
    assert "Ежемесячный платёж" in summary
    assert "1 000 000" not in summary  # проверяем формат с пробелами
    assert "1 000000" not in summary


def test_format_schedule_table():
    """Форматирование таблицы."""
    result = calculate(amount=100_000, annual_rate=12.0, years=1)
    table = format_schedule_table(result.schedule, limit=3)
    
    assert "Месяц" in table
    assert "1" in table
    assert "2" in table
    assert "3" in table
    assert "и ещё 9 платежей" in table