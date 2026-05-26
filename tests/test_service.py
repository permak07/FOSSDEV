from unittest.mock import patch, MagicMock
import pytest
import requests

from src.service import fetch_text, frequency_analysis


def test_fetch_text_success():
    """Успешный HTTP-запрос возвращает текст."""
    mock_response = MagicMock()
    mock_response.text = "sample text"
    mock_response.raise_for_status = MagicMock()

    with patch("service.requests.get", return_value=mock_response) as mock_get:
        result = fetch_text("http://example.com")
        mock_get.assert_called_once_with("http://example.com")
        assert result == "sample text"
        mock_response.raise_for_status.assert_called_once()


def test_fetch_text_failure():
    """При HTTP-ошибке исключение прокидывается выше."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404")

    with patch("service.requests.get", return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            fetch_text("http://example.com")


def test_frequency_analysis():
    """Частотный анализ считает повторы слов."""
    text = "foo bar foo"
    result = frequency_analysis(text)
    assert result == {"foo": 2, "bar": 1}
