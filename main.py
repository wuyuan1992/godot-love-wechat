from nicegui import ui, app
from app.layout import layout
from app.settings import settings
from app.project_list import project_list
from app.project import project

app.add_static_files("/assets", "assets")

@ui.page("/")
def index_page():
    with layout("home"):
        project_list()

@ui.page("/settings")
def settings_page():
    with layout("setting"):
        settings()

@ui.page("/projects/{id}")
def project_page(id: str):
    with layout("project"):
        project(id)

        

ui.run(port=24512, title="Godot Love Wechat", window_size=(1024, 768), native=True)
