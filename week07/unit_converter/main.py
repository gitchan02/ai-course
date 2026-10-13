# main.py
import flet as ft

import logic


def main(page: ft.Page):
    page.title = "단위 변환기"
    page.window.width = 360
    page.window.height = 480
    page.window.resizable = False

    value = ft.TextField(label="값", value="100", width=150)
    from_unit = ft.Dropdown(
        label="단위",
        value="cm",
        width=120,
        options=[ft.dropdown.Option(u) for u in logic.UNITS],
    )
    result = ft.Text(value="", size=20, weight=ft.FontWeight.BOLD, expand=True)
    to_unit = ft.Dropdown(
        label="단위",
        value="m",
        width=120,
        options=[ft.dropdown.Option(u) for u in logic.UNITS],
    )
    notice = ft.Text(value="", color=ft.Colors.RED)

    def on_convert(e):
        result.value, notice.value = logic.convert(
            value.value, from_unit.value, to_unit.value
        )
        page.update()

    page.add(
        ft.Row(controls=[value, from_unit]),
        ft.Text(value="↓"),
        ft.Row(controls=[ft.Text(value="결과"), result, to_unit]),
        ft.Button(
            content="변환",
            on_click=on_convert,
            expand=True,
            height=44,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
        ),
        notice,
    )


ft.run(main)
