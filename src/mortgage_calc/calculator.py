"""Ядро расчётов ипотеки."""

from decimal import ROUND_HALF_UP, Decimal

from mortgage_calc.types import Payment, PaymentSchedule


def calculate(
    amount: float,
    annual_rate: float,
    years: int,
) -> PaymentSchedule:
    """
    Рассчитать аннуитетный кредит.

    Args:
        amount: Сумма кредита
        annual_rate: Годовая процентная ставка (например, 7.5)
        years: Срок в годах

    Returns:
        PaymentSchedule с полным графиком платежей

    Raises:
        ValueError: При некорректных входных данных
    """
    if amount <= 0:
        raise ValueError("Сумма кредита должна быть положительной")
    if annual_rate < 0:
        raise ValueError("Процентная ставка не может быть отрицательной")
    if years <= 0:
        raise ValueError("Срок кредита должен быть положительным")

    months = years * 12
    monthly_rate = Decimal(str(annual_rate)) / Decimal("100") / Decimal("12")

    amount_d = Decimal(str(amount))

    if monthly_rate == 0:
        monthly_payment = amount_d / Decimal(str(months))
    else:
        factor = (Decimal("1") + monthly_rate) ** months
        monthly_payment = amount_d * monthly_rate * factor / (factor - Decimal("1"))

    monthly_payment = monthly_payment.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    schedule: list[Payment] = []
    remaining_balance: Decimal = amount_d

    for month in range(1, months + 1):
        interest = (remaining_balance * monthly_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        if month == months:
            principal = remaining_balance
            total = principal + interest
            next_balance: Decimal = Decimal("0")
        else:
            principal = monthly_payment - interest
            if principal > remaining_balance:
                principal = remaining_balance
            total = principal + interest
            next_balance = (remaining_balance - principal).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

        schedule.append(
            Payment(
                month=month,
                total=float(total),
                principal=float(principal),
                interest=float(interest),
                remaining=float(next_balance),
            )
        )
        remaining_balance = next_balance

    total_payment: Decimal = sum(
        (Decimal(str(p.total)) for p in schedule),
        Decimal("0"),
    )
    total_interest: Decimal = sum(
        (Decimal(str(p.interest)) for p in schedule),
        Decimal("0"),
    )

    return PaymentSchedule(
        monthly_payment=float(monthly_payment),
        total_payment=float(total_payment.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        total_interest=float(total_interest.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        schedule=schedule,
    )
