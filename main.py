import os
import plistlib

from plugin import PlugIn
from plugin_format import PluginFormat


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


if __name__ == "__main__":
    path_to_all_plugins = "/Library/Audio/Plug-Ins/"
    info_plist_suffix = "/Contents/Info.plist"

    for file_path in plugin_file_paths(path_to_all_plugins, PluginFormat.all()):
        plugin = PlugIn.from_path(file_path, read_plist_file(info_plist_suffix))
        print(plugin)
