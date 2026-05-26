import requests
import numpy as np
import fastapi

app = fastapi.FastAPI()


def fetch_text(url: str) -> str:
    """Получение текста из URL-адреса."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def frequency_analysis(text: str) -> dict[str, int]:
    """Подсчёт частоты встречаемости слов с помощью библиотеки numpy"""
    words = text.lower().split()
    unique, counts = np.unique(words, return_counts=True)
    return dict(zip(unique, counts))
