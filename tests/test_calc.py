import pytest
from src.calc import count_words, avg_word_length

def test_count_words_empty():
    """Пустая строка даёт 0 слов."""
    assert count_words("") == 0


def test_count_words_simple():
    """Обычная строка разбивается по пробелам."""
    assert count_words("hello world foo") == 3


def test_avg_word_length_empty():
    """Пустой список даёт 0.0."""
    assert avg_word_length([]) == 0.0


def test_avg_word_length_simple():
    """Средняя длина считается корректно."""
    words = ["abcd", "efgh", "ij"]
    # (4 + 4 + 2) / 3 == 10 / 3
    assert avg_word_length(words) == pytest.approx(10 / 3)
