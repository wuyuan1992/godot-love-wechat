from dataclasses import dataclass
from nicegui import ui, app
from app.stroge import Storge
import webview

@dataclass
class SettingsItem:
    godot_execute: str
    wechat_execute: str

def settings():
    setting_item = SettingsItem(godot_execute="", wechat_execute="")
    storge = Storge()
    settings_data = storge.get("settings.json")

    if settings_data:
        setting_item.godot_execute = settings_data["godot_execute"]
        setting_item.wechat_execute = settings_data["wechat_execute"]

    def save_settings():
        storge.save("settings.json", {"godot_execute": setting_item.godot_execute, "wechat_execute": setting_item.wechat_execute })
        

    async def choose_godot():
        file_types = ('Godot Execute (*.exe)',)
        file = await app.native.main_window.create_file_dialog(dialog_type=webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types) # type: ignore
        setting_item.godot_execute = file[0]

    async def choose_wechat():
        file = await app.native.main_window.create_file_dialog(dialog_type=webview.FOLDER_DIALOG, allow_multiple=False, file_types=()) # type: ignore
        setting_item.wechat_execute = file[0]

    with ui.column(align_items="start").classes("w-full p-2"):
        with ui.row().classes("border-b pb-2 w-full"):
            ui.markdown("### 设置")
        with ui.input(placeholder="godot引擎的执行目录，用来导出pck包", label="godot引擎").classes("w-full") as i:
            i.bind_value(setting_item, "godot_execute")
            ui.button(icon="folder_open", on_click=choose_godot).props("flat dense")
        
        with ui.input(placeholder="微信开发者工具目录，用来预览小游戏", label="微信开发者工具目录").classes("w-full") as i:
            i.bind_value(setting_item, "wechat_execute")
            ui.button(icon="folder_open", on_click=choose_wechat).props("flat dense")

        with ui.column(align_items="end").classes("w-full mt-4"):
            ui.button("保存", icon="save", on_click=save_settings)
