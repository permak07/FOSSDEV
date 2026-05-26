"""Математические операции для анализа текста."""

def count_words(text: str) -> int:
    """Кол-во слов в тексте."""
    return len(text.split())

def avg_word_length(words: list[str]) -> float:
    """Подсёт средней длины слов"""
    if not words:
        return 0.0
    total = sum(len(word) for word in words)
    return total / len(words)