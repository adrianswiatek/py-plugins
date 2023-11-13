from plugin_format import PluginFormat


class PlugIn(object):
    def __init__(self, name, version, plugin_format, file_path):
        self.name = name
        self.version = version
        self.plugin_format = plugin_format
        self.file_path = file_path

    def __str__(self):
        name = f"name={self.name}"
        version = f"version={self.version}"
        plugin_format = f"plugin_format={self.plugin_format}"
        file_path = f"file_path={self.file_path}"
        return f"Plugin[{name}, {version}, {plugin_format}, {file_path}]"

    @staticmethod
    def from_path(path_to_plugin, read_file):
        def first_existing_key(keys, file):
            if len(keys) == 0:
                return None
            elif len(keys) == 1 or keys[0] in file:
                return file[keys[0]]
            else:
                return first_existing_key(keys[1:], file)

        plist_file = read_file(path_to_plugin)

        if plist_file is None:
            return "--- " + path_to_plugin

        plugin_format = PluginFormat.from_path(path_to_plugin)

        name = first_existing_key(["CFBundleName", "CFBundleExecutable"], plist_file)
        version = first_existing_key(["CFBundleShortVersionString", "CFBundleVersion"], plist_file)

        return PlugIn(name=name, version=version, plugin_format=plugin_format, file_path=path_to_plugin)