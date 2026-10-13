import math

UNITS = ["mm", "cm", "m", "km", "°C", "°F"]

METERS = {"mm": 0.001, "cm": 0.01, "m": 1, "km": 1000}
TEMPERATURES = ("°C", "°F")

NOT_NUMBER = "숫자를 입력하세요"
MIXED = "길이와 온도는 서로 변환할 수 없습니다"
NEGATIVE_LENGTH = "길이는 0 이상이어야 합니다"
TOO_BIG = "값이 너무 큽니다"


def format_number(x):
    text = f"{x:.6f}".rstrip("0").rstrip(".")
    if text in ("", "-0"):
        return "0"
    return text


def _parse(text):
    text = text.strip()
    if not text.isascii() or "_" in text:
        return None
    try:
        value = float(text)
    except ValueError:
        return None
    if not math.isfinite(value):
        return None
    return value


def _calculate(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit in METERS:
        return value * METERS[from_unit] / METERS[to_unit]
    if from_unit == "°C":
        return value * 9 / 5 + 32
    return (value - 32) * 5 / 9


def convert(text, from_unit, to_unit):
    value = _parse(text)
    if value is None:
        return "", NOT_NUMBER
    if (from_unit in TEMPERATURES) != (to_unit in TEMPERATURES):
        return "", MIXED
    if from_unit in METERS and value < 0:
        return "", NEGATIVE_LENGTH
    result = _calculate(value, from_unit, to_unit)
    if not math.isfinite(result):
        return "", TOO_BIG
    return format_number(result), ""
