from nicegui import ui


def project(id: str):
    with ui.column(align_items="start").classes("w-full p-2"):
        ui.label(id)

