import unittest

import logic


class ParseGuessTest(unittest.TestCase):
    def test_valid(self):
        cases = [
            ("50", 50),
            ("1", 1),
            ("100", 100),
            (" 50 ", 50),
            ("007", 7),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(logic.parse_guess(text), expected)

    def test_invalid(self):
        cases = [
            "", "   ", "abc", "5a", "5.0", "50.5",
            "-5", "+7", "0", "101", "1e2", "５０",
        ]
        for text in cases:
            with self.subTest(text=text):
                with self.assertRaises(ValueError) as ctx:
                    logic.parse_guess(text)
                self.assertEqual(str(ctx.exception), "1~100 사이의 정수를 입력하세요")


class JudgeTest(unittest.TestCase):
    def test_judge(self):
        cases = [
            (30, 50, "더 큽니다"),
            (70, 50, "더 작습니다"),
            (50, 50, "정답입니다"),
            (1, 100, "더 큽니다"),
            (100, 1, "더 작습니다"),
        ]
        for guess, answer, expected in cases:
            with self.subTest(guess=guess, answer=answer):
                self.assertEqual(logic.judge(guess, answer), expected)


class FormatRecordTest(unittest.TestCase):
    def test_format_record(self):
        cases = [
            (50, "더 큽니다", "50 (더 큽니다)"),
            (100, "더 작습니다", "100 (더 작습니다)"),
            (42, "정답입니다", "42 (정답입니다)"),
        ]
        for guess, verdict, expected in cases:
            with self.subTest(guess=guess):
                self.assertEqual(logic.format_record(guess, verdict), expected)


class UpdateBestTest(unittest.TestCase):
    def test_update_best(self):
        cases = [
            (None, 5, 5),
            (10, 5, 5),
            (5, 10, 5),
            (5, 5, 5),
            (1, 7, 1),
        ]
        for best, tries, expected in cases:
            with self.subTest(best=best, tries=tries):
                self.assertEqual(logic.update_best(best, tries), expected)


class NewAnswerTest(unittest.TestCase):
    def test_range(self):
        for _ in range(1000):
            value = logic.new_answer()
            self.assertIsInstance(value, int)
            self.assertTrue(1 <= value <= 100, value)


if __name__ == "__main__":
    unittest.main()
