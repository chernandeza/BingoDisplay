from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

DATA_FILE = Path("data/called_numbers.json")
called_numbers: list[int] = []


def load_called_numbers() -> list[int]:
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text())
            return [value for value in data if isinstance(value, int) and 1 <= value <= 75]
        except json.JSONDecodeError:
            return []
    return []


def save_called_numbers(values: list[int]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(values))


called_numbers = load_called_numbers()


def number_to_letter(value: int) -> str:
    if 1 <= value <= 15:
        return "B"
    if 16 <= value <= 30:
        return "I"
    if 31 <= value <= 45:
        return "N"
    if 46 <= value <= 60:
        return "G"
    if 61 <= value <= 75:
        return "O"
    raise ValueError("Number out of range for Bingo")


def normalize_number(raw: str) -> int | None:
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return None
    if 1 <= value <= 75:
        return value
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    message = request.args.get("message") or None
    last_call = called_numbers[-1] if called_numbers else None

    if request.method == "POST":
        raw_number = request.form.get("number")
        value = normalize_number(raw_number)

        if value is None:
            message = "Please enter a valid number between 1 and 75."
        elif value in called_numbers:
            message = f"{number_to_letter(value)}{value} has already been called."
        else:
            called_numbers.append(value)
            save_called_numbers(called_numbers)
            return redirect(url_for("index"))

        last_call = value if value is not None else last_call

    board_columns = {
        "B": list(range(1, 16)),
        "I": list(range(16, 31)),
        "N": list(range(31, 46)),
        "G": list(range(46, 61)),
        "O": list(range(61, 76)),
    }

    return render_template(
        "index.html",
        message=message,
        last_call=last_call,
        called_numbers=set(called_numbers),
        board_columns=board_columns,
        number_to_letter=number_to_letter,
    )


@app.route("/reset", methods=["POST"])
def reset_board():
    called_numbers.clear()
    save_called_numbers(called_numbers)
    return redirect(url_for("index", message="Board cleared."))


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
