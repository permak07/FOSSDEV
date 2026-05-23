"""Фикстуры для тестов."""

import pytest

from src.mortgage_calc.calculator import calculate


@pytest.fixture
def sample_mortgage():
    """Стандартный пример ипотеки."""
    return calculate(amount=1_000_000, annual_rate=12.0, years=1)