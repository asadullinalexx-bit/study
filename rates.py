"""Получение курсов валют через open.er-api.com (без API-ключа)."""
import requests

API_URL = "https://open.er-api.com/v6/latest/{base}"


def get_rates(base="USD"):
    """Возвращает словарь курсов относительно базовой валюты.

    Например get_rates("USD") -> {"EUR": 0.92, "RUB": 78.5, ...}
    """
    response = requests.get(API_URL.format(base=base.upper()), timeout=10)
    data = response.json()
    if data.get("result") != "success":
        raise RuntimeError(f"API вернул ошибку: {data.get('error-type', 'unknown')}")
    return data["rates"]
