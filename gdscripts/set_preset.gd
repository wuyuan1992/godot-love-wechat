extends SceneTree


func _init() -> void:
	var args = OS.get_cmdline_user_args()
	var config = ConfigFile.new()
	var err = config.load("res://export_presets.cfg")
	if err != OK:
		return
	print(args)
	if args.size() == 1:
		var name = args[0]
		for section in config.get_sections():
			if section.begins_with("preset."):  # 找到所有 preset.x
				var _name = config.get_value(section, "name", "")
				if name == _name:
					config.set_value(section, "export_filter", "all_resources")
					if config.get_value(section, "export_files", ""):
						config.erase_section_key(section, "export_files")
					config.save("res://export_presets.cfg")
					quit()
					return
	if args.size() == 2:
		var name = args[0]
		var index = int(args[1])
		var export_settings = load_json_file("res://minigame.export.json")
		var subpack_configs = export_settings["subpack_config"]
		for section in config.get_sections():
			if section.begins_with("preset."):  # 找到所有 preset.x
				var _name = config.get_value(section, "name", "")
				if name == _name:
					var subpack_config = subpack_configs[index]
					var resources = PackedStringArray()
					resources.append_array(subpack_config["subpack_resource"])
					config.set_value(section, "export_filter", "resources")
					config.set_value(section, "export_files", resources)
					config.save("res://export_presets.cfg")
					quit()
					return


func load_json_file(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}

	var file = FileAccess.open(path, FileAccess.READ)
	var content = file.get_as_text()  # 读取整个 JSON 文件
	file.close()

	var data = JSON.parse_string(content)
	if data == null:
		return {}

	return data
