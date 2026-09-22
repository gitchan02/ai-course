import flet as ft

from calc import Calculator


def main(page: ft.Page):
    page.title = "계산기"
    page.window.width = 340
    page.window.height = 520
    page.window.resizable = False

    calculator = Calculator()
    display = ft.Text(value=calculator.display, size=40, text_align=ft.TextAlign.RIGHT)

    def press(key):
        calculator.press(key)
        display.value = calculator.display
        page.update()

    def on_button(e):
        press(e.control.data)

    def on_key(e: ft.KeyboardEvent):
        key = e.key
        if key == "Enter":
            key = "="
        elif key == "Backspace":
            key = "BS"
        elif key == "Escape":
            key = "C"
        press(key)

    page.on_keyboard_event = on_key

    def make_button(label, key, bgcolor):
        return ft.Button(content=label, data=key, on_click=on_button, expand=1, height=60,
                         bgcolor=bgcolor, color=ft.Colors.WHITE)

    rows = [
        [("C", "C", ft.Colors.GREY_600), ("+/-", "+/-", ft.Colors.GREY_600),
         ("%", "%", ft.Colors.GREY_600), ("÷", "/", ft.Colors.ORANGE)],
        [("7", "7", ft.Colors.GREY_800), ("8", "8", ft.Colors.GREY_800),
         ("9", "9", ft.Colors.GREY_800), ("×", "*", ft.Colors.ORANGE)],
        [("4", "4", ft.Colors.GREY_800), ("5", "5", ft.Colors.GREY_800),
         ("6", "6", ft.Colors.GREY_800), ("−", "-", ft.Colors.ORANGE)],
        [("1", "1", ft.Colors.GREY_800), ("2", "2", ft.Colors.GREY_800),
         ("3", "3", ft.Colors.GREY_800), ("+", "+", ft.Colors.ORANGE)],
        [("0", "0", ft.Colors.GREY_800), (".", ".", ft.Colors.GREY_800),
         ("⌫", "BS", ft.Colors.GREY_800), ("=", "=", ft.Colors.ORANGE)],
    ]

    controls = [ft.Container(content=display, alignment=ft.Alignment.CENTER_RIGHT, padding=10, height=90)]
    for row in rows:
        controls.append(ft.Row(controls=[make_button(label, key, color) for label, key, color in row]))
    page.add(*controls)


ft.run(main)