# main.py
import flet as ft

import logic

TEXT_COLOR = "#222222"
GRAY_TEXT = "#666666"
GRAY_BORDER = "#999999"
BLUE = "#2F6FDE"
DARK_GRAY = "#555555"


def main(page: ft.Page):
    page.title = "숫자 맞히기"
    page.window.width = 480
    page.window.height = 560
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#FAFAFA"
    page.padding = 24

    answer = logic.new_answer()
    tries = 0
    finished = False
    best = None

    button_shape = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))

    guess = ft.TextField(
        label="숫자",
        value="",
        expand=True,
        height=48,
        border=ft.OutlineInputBorder(
            side=ft.BorderSide(1, GRAY_BORDER), border_radius=8
        ),
        color=TEXT_COLOR,
    )
    notice = ft.Text(value="", color=ft.Colors.RED)
    result = ft.Text(value="", size=32, weight=ft.FontWeight.BOLD, color=TEXT_COLOR)
    tries_text = ft.Text(value="시도 횟수: 0", color=GRAY_TEXT)
    best_text = ft.Text(value="최고 기록: 없음", color=GRAY_TEXT)
    items = ft.ListView(expand=True, spacing=4)

    def on_guess(e):
        nonlocal tries, finished, best
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
            0, ft.Text(value=logic.format_record(number, verdict), color=TEXT_COLOR)
        )
        tries_text.value = f"시도 횟수: {tries}"
        notice.value = ""
        guess.value = ""
        result.value = verdict
        if verdict == "정답입니다":
            finished = True
            best = logic.update_best(best, tries)
            best_text.value = f"최고 기록: {best}번"
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
        ft.Text(value="1부터 100 사이의 숫자를 맞힙니다.", color=TEXT_COLOR),
        ft.Row(
            controls=[
                guess,
                ft.Button(
                    content=ft.Text(value="확인", weight=ft.FontWeight.BOLD),
                    on_click=on_guess,
                    width=110,
                    height=48,
                    bgcolor=BLUE,
                    color=ft.Colors.WHITE,
                    style=button_shape,
                ),
            ]
        ),
        notice,
        result,
        tries_text,
        best_text,
        ft.Container(
            content=items,
            height=150,
            padding=10,
            border=ft.Border.all(1, GRAY_BORDER),
            border_radius=8,
        ),
        ft.Row(
            controls=[
                ft.Button(
                    content=ft.Text(value="새 게임", weight=ft.FontWeight.BOLD),
                    on_click=on_new_game,
                    expand=True,
                    height=48,
                    bgcolor=DARK_GRAY,
                    color=ft.Colors.WHITE,
                    style=button_shape,
                )
            ]
        ),
    )


ft.run(main)
