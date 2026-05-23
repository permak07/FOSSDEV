"""Тесты расчётов."""

import pytest

from src.mortgage_calc.calculator import calculate
from src.mortgage_calc.types import PaymentSchedule


def test_basic_calculation():
    """Базовый расчёт на 1 год."""
    result = calculate(amount=1_000_000, annual_rate=12.0, years=1)
    
    assert isinstance(result, PaymentSchedule)
    assert result.monthly_payment == 88848.79
    assert len(result.schedule) == 12
    assert result.schedule[-1].remaining == 0.0


def test_zero_rate():
    """Кредит под 0%%."""
    result = calculate(amount=1_200_000, annual_rate=0.0, years=1)
    
    assert result.monthly_payment == 100000.00
    assert result.total_interest == 0.0


def test_long_term():
    """Долгосрочная ипотека."""
    result = calculate(amount=5_000_000, annual_rate=7.5, years=20)
    
    assert len(result.schedule) == 240
    assert result.schedule[-1].remaining == 0.0
    assert result.total_payment > result.total_interest > 0


def test_invalid_amount():
    """Отрицательная сумма."""
    with pytest.raises(ValueError, match="положительной"):
        calculate(amount=-1000, annual_rate=10, years=5)


def test_invalid_rate():
    """Отрицательная ставка."""
    with pytest.raises(ValueError, match="отрицательной"):
        calculate(amount=1000, annual_rate=-1, years=5)


def test_invalid_years():
    """Нулевой срок."""
    with pytest.raises(ValueError, match="положительным"):
        calculate(amount=1000, annual_rate=10, years=0)


def test_schedule_consistency():
    """Проверка целостности графика."""
    result = calculate(amount=2_000_000, annual_rate=9.0, years=5)
    
    # Сумма всех платежей по основному долгу = сумма кредита
    total_principal = sum(p.principal for p in result.schedule)
    assert abs(total_principal - 2_000_000) < 0.1
    
    # Последний остаток = 0
    assert result.schedule[-1].remaining == 0.0