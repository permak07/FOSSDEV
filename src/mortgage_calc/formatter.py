"""Форматирование результатов."""

from mortgage_calc.types import Payment, PaymentSchedule


def format_currency(value: float) -> str:
    """Отформатировать сумму в рублях."""
    return f"{value:,.2f} ₽".replace(",", " ")


def format_percent(value: float) -> str:
    """Отформатировать процент."""
    return f"{value:.2f}%"


def format_schedule_table(schedule: list[Payment], limit: int | None = None) -> str:
    """Сформировать текстовую таблицу графика платежей."""
    lines = [
        f"{'Месяц':>6} │ {'Платёж':>12} │ {'Основной долг':>14} │ "
        f"{'Проценты':>12} │ {'Остаток':>12}",
        "─" * 75,
    ]

    display = schedule[:limit] if limit else schedule
    for p in display:
        lines.append(
            f"{p.month:>6} │ {p.total:>12,.2f} │ {p.principal:>14,.2f} │ "
            f"{p.interest:>12,.2f} │ {p.remaining:>12,.2f}"
        )

    if limit and len(schedule) > limit:
        lines.append(f"\n... и ещё {len(schedule) - limit} платежей")

    return "\n".join(lines)


def format_summary(result: PaymentSchedule) -> str:
    """Сформировать сводку по кредиту."""
    return (
        f"Ежемесячный платёж: {format_currency(result.monthly_payment)}\n"
        f"Общая сумма выплат:  {format_currency(result.total_payment)}\n"
        f"Переплата:           {format_currency(result.total_interest)}\n"
        f"Процент переплаты:   {format_percent(result.total_interest / result.total_payment * 100)}"
    )
