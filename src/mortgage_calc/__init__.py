"""Ипотечный калькулятор."""

__version__ = "0.1.0"
__all__ = ["calculate", "Payment", "PaymentSchedule"]

from mortgage_calc.calculator import calculate
from mortgage_calc.types import Payment, PaymentSchedule