"""Типы данных для ипотечного калькулятора."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Payment:
    """Один платёж по графику."""
    
    month: int
    total: float
    principal: float
    interest: float
    remaining: float


@dataclass(frozen=True)
class PaymentSchedule:
    """Результат расчёта ипотеки."""
    
    monthly_payment: float
    total_payment: float
    total_interest: float
    schedule: List[Payment]