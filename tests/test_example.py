from src.example import show_summary

def test_show_summary():
    """Форматированная строка собирается правильно."""
    result = show_summary(100, 4.5, "hello")
    assert result == "Words: 100, Avg: 4.50, Top: hello"
