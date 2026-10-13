# main.py
import flet as ft

import logic


def main(page: ft.Page):
    page.title = "숫자 맞히기"
    page.window.width = 400
    page.window.height = 600
    page.window.resizable = False

    answer = logic.new_answer()
    tries = 0
    finished = False

    tries_text = ft.Text(value="시도 횟수: 0", size=20, weight=ft.FontWeight.BOLD)
    guess = ft.TextField(label="숫자", value="", width=200)
    notice = ft.Text(value="", color=ft.Colors.RED)
    result = ft.Text(value="", size=20, weight=ft.FontWeight.BOLD)
    items = ft.ListView(expand=True, spacing=4)

    def on_guess(e):
        nonlocal tries, finished
        if finished:
            return
        try:
            number = logic.parse_guess(guess.value)
        except ValueError as err:
            notice.value = str(err)
            page.update()
            return

        tries += 1
        verdict = logic.judge(number, answer)
        items.controls.insert(
            0, ft.Text(value=logic.format_record(tries, number, verdict))
        )
        tries_text.value = f"시도 횟수: {tries}"
        notice.value = ""
        guess.value = ""
        if verdict == "정답입니다":
            finished = True
            result.value = f"{tries}번 만에 맞혔습니다!"
        page.update()

    def on_new_game(e):
        nonlocal answer, tries, finished
        answer = logic.new_answer()
        tries = 0
        finished = False
        items.controls.clear()
        tries_text.value = "시도 횟수: 0"
        notice.value = ""
        result.value = ""
        guess.value = ""
        page.update()

    page.add(
        ft.Text(value="숫자 맞히기", size=24, weight=ft.FontWeight.BOLD),
        ft.Text(value="1부터 100 사이의 숫자를 맞혀 보세요"),
        tries_text,
        ft.Row(
            controls=[
                guess,
                ft.Button(
                    content="확인",
                    on_click=on_guess,
                    expand=True,
                    height=44,
                    bgcolor=ft.Colors.BLUE,
                    color=ft.Colors.WHITE,
                ),
            ]
        ),
        notice,
        result,
        ft.Button(content="새 게임", on_click=on_new_game, height=44),
        items,
    )


ft.run(main)
