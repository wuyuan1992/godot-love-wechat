from contextlib import contextmanager
from nicegui import ui, context
from app.menu import menu

@contextmanager
def layout(page: str):
    context.client.content.classes("h-[100vh] p-0")
    ui.colors(
        primary="#81a1c1",
        secondary="#5e81ac",
        accent="#81a1c1",
        positive="#a3be8c",
        dark="#434c5e",
        dark_page="#3b4252",
        negative="#bf616a",
        info="#a3be8c",
        warning="ebcb8b",
        light = "#eceff4",
        backgroud = "#d8dee9",
    )
    with ui.row(wrap=False).classes("h-full w-full"):
        with ui.column().classes("w-1/5 h-full p-2").style("background-color: #434c5e"):
            menu()
        with ui.column().classes("w-4/5 h-full w-full p-2"):
            yield

