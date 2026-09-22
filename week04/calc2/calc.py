class Calculator:
    def __init__(self):
        self._reset()

    @property
    def display(self):
        return self._display

    def _reset(self):
        self._display = "0"
        self._accumulator = None
        self._operator = None
        self._waiting_for_operand = False
        self._just_evaluated = False
        self._error = False

    def _number(self):
        return float(self._display)

    def _format_number(self, value):
        rounded = round(value, 10)
        if rounded == 0:
            return "0"
        text = format(rounded, ".10f").rstrip("0").rstrip(".")
        return text

    def _calculate(self, left, operator, right):
        if operator == "+":
            return left + right
        if operator == "-":
            return left - right
        if operator == "*":
            return left * right
        if operator == "/":
            if right == 0:
                self._display = "0으로 나눌 수 없습니다"
                self._error = True
                return None
            return left / right
        return right

    def _start_new_number(self, digit):
        self._display = digit
        self._waiting_for_operand = False
        self._just_evaluated = False

    def _input_digit(self, digit):
        if self._just_evaluated:
            self._accumulator = None
            self._operator = None
            self._start_new_number(digit)
            return
        if self._waiting_for_operand:
            self._start_new_number(digit)
            return
        digits = self._display.replace(".", "").replace("-", "")
        if len(digits) >= 12:
            return
        if self._display in ("0", "-0"):
            self._display = "-" + digit if self._display == "-0" else digit
        else:
            self._display += digit

    def _input_decimal(self):
        if self._just_evaluated:
            self._accumulator = None
            self._operator = None
            self._display = "0."
            self._just_evaluated = False
            return
        if self._waiting_for_operand:
            self._display = "0."
            self._waiting_for_operand = False
            return
        if "." not in self._display:
            self._display += "."

    def _input_operator(self, operator):
        if self._just_evaluated:
            self._accumulator = self._number()
            self._just_evaluated = False
        if self._accumulator is None:
            self._accumulator = self._number()
        elif not self._waiting_for_operand:
            result = self._calculate(self._accumulator, self._operator, self._number())
            if result is None:
                return
            self._accumulator = result
            self._display = self._format_number(result)
        self._operator = operator
        self._waiting_for_operand = True

    def _input_equals(self):
        if self._accumulator is None or self._operator is None or self._waiting_for_operand:
            return
        result = self._calculate(self._accumulator, self._operator, self._number())
        if result is None:
            return
        self._display = self._format_number(result)
        self._accumulator = None
        self._operator = None
        self._waiting_for_operand = False
        self._just_evaluated = True

    def _backspace(self):
        if self._just_evaluated or self._waiting_for_operand:
            return
        if len(self._display) <= 1 or self._display in ("-0", "0."):
            self._display = "0"
            return
        self._display = self._display[:-1]
        if self._display in ("", "-", "-0"):
            self._display = "0"

    def _toggle_sign(self):
        if self._just_evaluated:
            self._just_evaluated = False
        if self._waiting_for_operand:
            self._display = "-0"
            self._waiting_for_operand = False
        elif self._display.startswith("-"):
            self._display = self._display[1:]
        elif self._display != "0":
            self._display = "-" + self._display

    def _percent(self):
        if self._waiting_for_operand:
            return
        self._display = self._format_number(self._number() / 100)
        self._just_evaluated = False

    def press(self, key: str):
        if key == "C":
            self._reset()
            return
        if self._error:
            return
        if key in "0123456789":
            self._input_digit(key)
        elif key == ".":
            self._input_decimal()
        elif key in ("+", "-", "*", "/"):
            self._input_operator(key)
        elif key == "=":
            self._input_equals()
        elif key == "BS":
            self._backspace()
        elif key == "+/-":
            self._toggle_sign()
        elif key == "%":
            self._percent()