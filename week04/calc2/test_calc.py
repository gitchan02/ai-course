from calc import Calculator


CASES = [
    ("", "0"),
    ("1 2 + 3 =", "15"),
    ("2 + 3 * 4 =", "20"),
    ("5 + - 3 =", "2"),
    ("0 . 1 + 0 . 2 =", "0.3"),
    ("6 / 3 =", "2"),
    ("7 / 2 =", "3.5"),
    ("5 / 0 =", "0으로 나눌 수 없습니다"),
    ("5 / 0 = 7", "0으로 나눌 수 없습니다"),
    ("5 / 0 = C", "0"),
    ("1 . . 5", "1.5"),
    (".", "0."),
    ("0 0 7", "7"),
    ("1 2 3 BS", "12"),
    ("5 BS", "0"),
    ("9 +/-", "-9"),
    ("5 0 %", "0.5"),
    ("2 + 3 = 4", "4"),
    ("2 + 3 = + 4 =", "9"),
    ("2 + 3 = =", "5"),
]


def run_case(sequence):
    calculator = Calculator()
    for key in sequence.split():
        calculator.press(key)
    return calculator.display


def main():
    failures = []
    for sequence, expected in CASES:
        actual = run_case(sequence)
        if actual != expected:
            failures.append((sequence or "(아무것도 누르지 않음)", expected, actual))
    if failures:
        for sequence, expected, actual in failures:
            print(f"실패: {sequence} / 기대값: {expected} / 실제값: {actual}")
        raise SystemExit(1)
    print(f"모든 테스트 통과 ({len(CASES)}개)")


if __name__ == "__main__":
    main()