"""Монитор курса валют.

Показывает текущие курсы выбранных валют к доллару и сравнивает
с прошлым запуском: история хранится в history.json.

Запуск: python main.py
"""
import json
import os
from datetime import datetime, timezone

from rates import get_rates

WATCHLIST = ["RUB", "EUR", "CHF", "CNY"]   # за какими валютами следим
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def main():
    rates = get_rates("USD")
    history = load_history()
    previous = history[-1]["rates"] if history else {}

    print(f"курс USD на {datetime.now():%d.%m.%Y %H:%M}")
    for currency in WATCHLIST:
        rate = rates[currency]
        if currency in previous:
            diff = rate - previous[currency]
            arrow = "^" if diff > 0 else "v" if diff < 0 else "="
            print(f"  {currency}: {rate:.4f}  {arrow} {diff:+.4f}")
        else:
            print(f"  {currency}: {rate:.4f}")

    history.append({
        "time": datetime.now(timezone.utc).isoformat(),
        "rates": {c: rates[c] for c in WATCHLIST},
    })
    save_history(history)
    print(f"история сохранена: {len(history)} запусков")


if __name__ == "__main__":
    main()
