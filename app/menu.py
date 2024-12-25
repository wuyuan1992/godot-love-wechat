from nicegui import ui

def menu():
    with ui.column().classes("items-start w-full h-full"):
        with ui.column(align_items="center").classes("w-full pb-8 pt-4"):
            ui.image("/assets/logo.svg").classes("w-16 h-16")
            ui.label("Godot ❤️  Wechat").classes("text-white")
        ui.button("项目", icon="grid_view", color="light", on_click=lambda: ui.navigate.to("/")).classes("w-full").props("flat")
        ui.space()
        ui.button("设置", icon="settings", color="light", on_click=lambda: ui.navigate.to("/settings")).classes("w-full").props("flat")
