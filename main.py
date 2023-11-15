import plistlib

from pathlib import Path
from plugin import PlugIn
from plugin_format import PluginFormat


def read_plist_file(path):
    info_plist_path = "/Contents/Info.plist"
    full_path = Path(str(path) + info_plist_path)

    if not full_path.is_file():
        return None

    with open(full_path, 'rb') as file:
        return plistlib.load(file)


def plugins_in_format(root_path):
    def wrapper(plugin_format):
        path_to_plugins = root_path / plugin_format.value
        return path_to_plugins.glob(f"**/*{plugin_format.file_suffix}") if path_to_plugins.exists() else []

    return wrapper


def flatten_paths(paths):
    paths = list(paths)

    if not len(paths):
        return []

    head = paths[0]
    tail = paths[1:]

    return list(head) + flatten_paths(tail)


def print_plugins(plugins):
    plugins = list(plugins)

    if not len(plugins):
        return

    head = plugins[0]
    tail = plugins[1:]

    if head is not None:
        print(head)

    print_plugins(tail)


if __name__ == "__main__":
    path_to_all_plugins = "/Library/Audio/Plug-Ins/"

    root_plugin_directory_path = Path(path_to_all_plugins)
    list_of_plugin_paths = map(plugins_in_format(root_plugin_directory_path), PluginFormat.all())
    plugin_paths = flatten_paths(list_of_plugin_paths)
    all_plugins = filter(lambda x: x is not None, map(PlugIn.from_path(read_plist_file), plugin_paths))
    all_sorted_plugins = sorted(all_plugins, key=lambda x: x.name)

    print_plugins(all_sorted_plugins)
