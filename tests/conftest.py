"""Фикстуры для тестов."""

from typing import Generator

import pytest

from mortgage_calc.calculator import calculate
from mortgage_calc.types import PaymentSchedule


@pytest.fixture
def sample_mortgage() -> PaymentSchedule:
    """Стандартный пример ипотеки."""
    return calculate(amount=1_000_000, annual_rate=12.0, years=1)