from logic import UNITS, convert


NOT_NUMBER = "숫자를 입력하세요"
MIXED = "길이와 온도는 서로 변환할 수 없습니다"
NEGATIVE_LENGTH = "길이는 0 이상이어야 합니다"
TOO_BIG = "값이 너무 큽니다"

# (값, 변환 전, 변환 후, 기대 결과, 기대 안내 문구)
CASES = [
    ("100", "cm", "m", "1", ""),
    ("1", "m", "cm", "100", ""),
    ("1", "km", "mm", "1000000", ""),
    ("1", "mm", "km", "0.000001", ""),
    ("1", "cm", "m", "0.01", ""),
    ("1", "mm", "cm", "0.1", ""),
    ("0.1", "m", "cm", "10", ""),
    ("2.5", "km", "m", "2500", ""),
    ("0", "cm", "m", "0", ""),
    ("-0", "cm", "m", "0", ""),
    ("100", "°C", "°F", "212", ""),
    ("0", "°C", "°F", "32", ""),
    ("32", "°F", "°C", "0", ""),
    ("1", "°F", "°C", "-17.222222", ""),
    ("-40", "°C", "°F", "-40", ""),
    ("-40", "°F", "°C", "-40", ""),
    ("-5", "°C", "°F", "23", ""),
    ("100", "cm", "cm", "100", ""),
    ("100", "°C", "°C", "100", ""),
    (" 12 ", "cm", "m", "0.12", ""),
    ("1e2", "cm", "m", "1", ""),
    ("0.0000001", "m", "m", "0", ""),
    ("-0.0000001", "°C", "°C", "0", ""),
    ("", "cm", "m", "", NOT_NUMBER),
    ("   ", "cm", "m", "", NOT_NUMBER),
    ("abc", "cm", "m", "", NOT_NUMBER),
    ("1,000", "cm", "m", "", NOT_NUMBER),
    ("1_000", "cm", "m", "", NOT_NUMBER),
    ("５０", "cm", "m", "", NOT_NUMBER),
    ("nan", "cm", "m", "", NOT_NUMBER),
    ("inf", "cm", "m", "", NOT_NUMBER),
    ("-inf", "cm", "m", "", NOT_NUMBER),
    ("abc", "cm", "°C", "", NOT_NUMBER),
    ("1", "cm", "°C", "", MIXED),
    ("1", "°F", "m", "", MIXED),
    ("-5", "cm", "°C", "", MIXED),
    ("-5", "cm", "m", "", NEGATIVE_LENGTH),
    ("1e308", "km", "mm", "", TOO_BIG),
]


def main():
    failures = []
    for text, from_unit, to_unit, expected_result, expected_notice in CASES:
        actual = convert(text, from_unit, to_unit)
        if actual != (expected_result, expected_notice):
            failures.append((text, from_unit, to_unit, (expected_result, expected_notice), actual))
    if UNITS != ["mm", "cm", "m", "km", "°C", "°F"]:
        failures.append(("UNITS", "", "", "여섯 개 단위", UNITS))
    if failures:
        for text, from_unit, to_unit, expected, actual in failures:
            print(f"실패: '{text}' {from_unit} → {to_unit} / 기대값: {expected} / 실제값: {actual}")
        raise SystemExit(1)
    print(f"모든 테스트 통과 ({len(CASES) + 1}개)")


if __name__ == "__main__":
    main()
