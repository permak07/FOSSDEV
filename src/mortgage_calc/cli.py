"""Командный интерфейс."""

import argparse
import json
import sys
from pathlib import Path

from mortgage_calc.calculator import calculate
from mortgage_calc.formatter import format_currency, format_schedule_table, format_summary


def create_parser() -> argparse.ArgumentParser:
    """Создать парсер аргументов."""
    parser = argparse.ArgumentParser(
        prog="mortgage",
        description="Ипотечный калькулятор",
    )
    parser.add_argument(
        "--amount", "-a",
        type=float,
        required=True,
        help="Сумма кредита",
    )
    parser.add_argument(
        "--rate", "-r",
        type=float,
        required=True,
        help="Годовая процентная ставка (%%)",
    )
    parser.add_argument(
        "--years", "-y",
        type=int,
        required=True,
        help="Срок кредита в годах",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json", "csv"],
        default="text",
        help="Формат вывода (по умолчанию: text)",
    )
    parser.add_argument(
        "--schedule", "-s",
        action="store_true",
        help="Показать полный график платежей",
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=12,
        help="Количество строк графика (по умолчанию: 12)",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Сохранить результат в файл",
    )
    return parser


def format_json(result) -> str:
    """Форматировать результат в JSON."""
    return json.dumps({
        "monthly_payment": result.monthly_payment,
        "total_payment": result.total_payment,
        "total_interest": result.total_interest,
        "schedule": [
            {
                "month": p.month,
                "total": p.total,
                "principal": p.principal,
                "interest": p.interest,
                "remaining": p.remaining,
            }
            for p in result.schedule
        ],
    }, indent=2, ensure_ascii=False)


def format_csv(result) -> str:
    """Форматировать график в CSV."""
    lines = ["month,total,principal,interest,remaining"]
    for p in result.schedule:
        lines.append(f"{p.month},{p.total},{p.principal},{p.interest},{p.remaining}")
    return "\n".join(lines)


def main() -> None:
    """Точка входа CLI."""
    # Windows: cp1251 не знает символ ₽, переключаем stdout/stderr в UTF-8
    if sys.platform == "win32":
        try:
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8")
                sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        result = calculate(args.amount, args.rate, args.years)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    
    if args.format == "json":
        output = format_json(result)
    elif args.format == "csv":
        output = format_csv(result)
    else:
        lines = [format_summary(result)]
        if args.schedule:
            lines.append("")
            lines.append(format_schedule_table(result.schedule, args.limit))
        output = "\n".join(lines)
    
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"Результат сохранён в {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()