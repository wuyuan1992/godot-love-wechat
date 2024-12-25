from nicegui import ui, app
from app.layout import layout
from app.settings import settings

app.add_static_files("/assets", "assets")

@ui.page("/")
def index_page():
    with layout("home"):
        with ui.column().classes("w-full"):
            ui.label("content")

@ui.page("/settings")
def settings_page():
    with layout("setting"):
        settings()
        

ui.run(port=24512, title="Godot Love Wechat", window_size=(1024, 768), native=True)
