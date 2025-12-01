from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, url_for

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


@app.route("/")
def raiz():
    return redirect(url_for("tablero"))


@app.route("/ingresar", methods=["GET", "POST"])
def ingresar():
    mensaje = request.args.get("mensaje") or None
    ultima_llamada = called_numbers[-1] if called_numbers else None

    if request.method == "POST":
        raw_number = request.form.get("numero")
        value = normalize_number(raw_number)

        if value is None:
            mensaje = "Ingresa un número válido entre 1 y 75."
        elif value in called_numbers:
            mensaje = f"{number_to_letter(value)}{value} ya fue cantado."
        else:
            called_numbers.append(value)
            save_called_numbers(called_numbers)
            return redirect(url_for("ingresar"))

        ultima_llamada = value if value is not None else ultima_llamada

    board_columns = {
        "B": list(range(1, 16)),
        "I": list(range(16, 31)),
        "N": list(range(31, 46)),
        "G": list(range(46, 61)),
        "O": list(range(61, 76)),
    }

    return render_template(
        "ingresar.html",
        mensaje=mensaje,
        ultima_llamada=ultima_llamada,
        llamadas=set(called_numbers),
        columnas=board_columns,
        number_to_letter=number_to_letter,
    )


@app.route("/tablero")
def tablero():
    board_columns = {
        "B": list(range(1, 16)),
        "I": list(range(16, 31)),
        "N": list(range(31, 46)),
        "G": list(range(46, 61)),
        "O": list(range(61, 76)),
    }
    ultima_llamada = called_numbers[-1] if called_numbers else None

    return render_template(
        "tablero.html",
        ultima_llamada=ultima_llamada,
        llamadas=set(called_numbers),
        columnas=board_columns,
        number_to_letter=number_to_letter,
    )


@app.route("/reset", methods=["POST"])
def reset_board():
    called_numbers.clear()
    save_called_numbers(called_numbers)
    destino = request.form.get("destino") or "ingresar"
    return redirect(url_for(destino, mensaje="Tablero reiniciado."))


@app.route("/estado")
def estado():
    ultima_llamada = called_numbers[-1] if called_numbers else None
    return jsonify({
        "ultima_llamada": ultima_llamada,
        "llamadas": called_numbers,
    })


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
