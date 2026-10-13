import random

ERROR_MESSAGE = "1~100 사이의 정수를 입력하세요"


def new_answer():
    return random.randint(1, 100)


def parse_guess(text):
    text = text.strip()
    if not (text.isascii() and text.isdigit()):
        raise ValueError(ERROR_MESSAGE)
    value = int(text)
    if not 1 <= value <= 100:
        raise ValueError(ERROR_MESSAGE)
    return value


def judge(guess, answer):
    if guess < answer:
        return "더 큽니다"
    if guess > answer:
        return "더 작습니다"
    return "정답입니다"


def format_record(n, guess, verdict):
    return f"{n}회차 · {guess} · {verdict}"


def update_best(best, tries):
    if best is None or tries < best:
        return tries
    return best
