from enum import Enum


class PluginFormat(Enum):
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