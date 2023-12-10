import flet as ft

def btn_click(page, greetings, first_name_arg, last_name_arg):
    def handler(e):
        greetings.current.controls.append(
            ft.Text(f"Hello, {first_name_arg.current.value} {last_name_arg.current.value}!")
        )
        first_name_arg.current.value = ""
        last_name_arg.current.value = ""
        page.update()
        first_name_arg.current.focus()
    return handler


def main(page):
    first_name = ft.Ref[ft.TextField]()
    last_name = ft.Ref[ft.TextField]()
    greetings = ft.Ref[ft.Column]()

    page.add(
        ft.TextField(ref=first_name, label="First name", autofocus=True),
        ft.TextField(ref=last_name, label="Last name"),
        ft.ElevatedButton("Say hello!", on_click=btn_click(page, greetings, first_name, last_name)),
        ft.Column(ref=greetings),
    )


ft.app(target=main)
