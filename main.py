import enum
import os
import plistlib


class PluginFormat(enum.Enum):
    audio_unit = "Components"
    vst = "VST"
    vst3 = "VST3"

    def __str__(self):
        return self.name

    def to_dir_path(self, prefix):
        return prefix + self.value + "/"

    @staticmethod
    def all():
        return [PluginFormat.audio_unit, PluginFormat.vst, PluginFormat.vst3]

    @property
    def file_suffix(self):
        if self == PluginFormat.audio_unit:
            return ".component"
        else:
            return "." + self.value.lower()

    @staticmethod
    def from_path(path):
        def to_search_term(plugin_format):
            return '/' + plugin_format.value.lower() + '/'

        if to_search_term(PluginFormat.audio_unit) in path.lower():
            return PluginFormat.audio_unit

        if to_search_term(PluginFormat.vst) in path.lower():
            return PluginFormat.vst

        if to_search_term(PluginFormat.vst3) in path.lower():
            return PluginFormat.vst3

        return None


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


def read_plist_file(suffix):
    def wrapper(path):
        full_path = path + suffix
        if os.path.isfile(full_path):
            with open(full_path, 'rb') as file:
                return plistlib.load(file)
        else:
            return None

    return wrapper


def plugin_file_paths(path_to_plugins, plugin_formats):
    def to_full_path(path):
        return lambda file_name: path + file_name

    def from_paths_and_format(paths, plugin_format):
        paths = list(paths)

        if len(paths) == 0:
            return []

        head = paths[0]
        tail = paths[1:]

        if plugin_format.file_suffix in head:
            return [head] + from_paths_and_format(tail, plugin_format)
        elif os.path.isdir(head):
            deeper_file_paths = map(to_full_path(f"{head}/"), os.listdir(f"{head}/"))
            return from_paths_and_format(deeper_file_paths, plugin_format) + from_paths_and_format(tail, plugin_format)
        else:
            return from_paths_and_format(tail, plugin_format)

    def from_path_and_formats(plugins_path, formats):
        formats = list(formats)

        if len(formats) == 0:
            return []

        head = formats[0]
        tail = formats[1:]

        path_to_plugin_format = head.to_dir_path(plugins_path)
        file_paths = map(to_full_path(path_to_plugin_format), os.listdir(path_to_plugin_format))

        return from_paths_and_format(file_paths, head) + from_path_and_formats(plugins_path, tail)

    return from_path_and_formats(path_to_plugins, plugin_formats)


path_to_all_plugins = "/Library/Audio/Plug-Ins/"
info_plist_suffix = "/Contents/Info.plist"
file_paths = plugin_file_paths(path_to_all_plugins, PluginFormat.all())

for file_path in file_paths:
    plugin = PlugIn.from_path(file_path, read_plist_file(info_plist_suffix))
    print(plugin)
